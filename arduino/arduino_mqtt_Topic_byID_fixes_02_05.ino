#include <ESP8266WiFi.h>
#include <PubSubClient.h>

/*
* IDENTIFICATION INFORMATION:
*/
const int identificationNum = 1;
const char* clientID = "001";
const char* clientName = "YIEEE_Pixel_" + identificationNum;

/*
* WIFI INFORMATION:
*/
const char* ssid = "yale wireless";
const char* password =  "";

/*
* MQTT INFORMATION:
*/
const char* mqttServer = "farmer.cloudmqtt.com";    //35.239.98.209 for our python server    farmer.cloudmqtt.com for cloud mqtt
const int mqttPort = 14479;  
const char* mqttUser = "xoemllsy";     // yale for ours.    xoemllsy for cloud mqtt
const char* mqttPassword = "hdgazSRFNst3";    //lightsnstuff for ours,    hdgazSRFNst3 for cloudmqtt

/*
* COLOR PINS:
*/
const int R_pin = 12;
const int G_pin = 15;
const int B_pin = 16;

WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {

  Serial.begin(115200);

  //set up pins as lights and turn all off
  analogWriteRange(255);
  pinMode(R_pin, OUTPUT);
  pinMode(G_pin, OUTPUT);
  pinMode(B_pin, OUTPUT);
  analogWrite(R_pin, 255);
  analogWrite(G_pin, 255);
  analogWrite(B_pin, 255);
 
  connectToWifi();
}

/*
* Function called when new mqtt message is published to subscribed topic
*/
void callback(char* topic, byte* data, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for(int i = 0; i < length; i++) {
    Serial.print((char)data[i]);
  }
  Serial.println("");

  // change the lights based on the received color
  changeColors((char*)data);
  
  // New line
  Serial.println("---------->");
}
 
/*
* Processes and publishes data and refreshes the connection
*/ 
void loop() {
  client.loop();
  if (WiFi.status() != WL_CONNECTED) {
    connectToWifi();}
}




/*
* Convert string of hex-form "#ff00ff" to individual RGB values and turn on lights
*/
void changeColors(char command[]) {
  char r[] = "00";
  char g[] = "00";
  char b[] = "00";
  r[0] = command[0];
  r[1] = command[1];
  g[0] = command[2];
  g[1] = command[3];
  b[0] = command[4];
  b[1] = command[5];
  long int red, blue, green;
  red = strtol (r,NULL,16);
  green = strtol (g,NULL,16);
  blue = strtol (b,NULL,16);
  Serial.println(red);
  Serial.println(blue);
  Serial.println(green);

  analogWrite(R_pin, (abs (red - 255)));
  analogWrite(G_pin, (abs (green - 255)));
  analogWrite(B_pin, (abs (blue - 255)));

}


//flashes red green blue when connected
void testLights() {

  analogWrite(R_pin, 255);
  analogWrite(G_pin, 255);
  analogWrite(B_pin, 255);

  delay(100);


  analogWrite(R_pin, 0);
  delay(500);
  analogWrite(R_pin, 255);
  analogWrite(G_pin, 0);
  delay(500);
  analogWrite(G_pin, 255);
  analogWrite(B_pin, 0);
  delay(500);
  analogWrite(B_pin, 255);
}


//called in setup and when the connection is lost durring opperation
//connects to wifi, and broker
void connectToWifi(){
  // Loop until wifi connection succeeds
  analogWrite(B_pin, 255);
  analogWrite(R_pin, 255);
  analogWrite(G_pin, 255);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    //flash blue while connecting
    analogWrite(B_pin, 0);
    delay(500);
    analogWrite(B_pin, 255);
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  analogWrite(B_pin, 255);
  Serial.println("Connected to the WiFi network");

  // Set up connection to MQTT broker
  client.setServer(mqttServer, mqttPort);

  // Function to callback when new message is received
  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT Broker");
 
    // Connect to the MQTT broker with MQTT Information
    if (client.connect(clientName, mqttUser, mqttPassword)) {
      // Connection Succeed, callback function is called automatically when new message is detected
      Serial.println("Connected to MQTT Broker");
    } else {
      // MQTT connection failed
      Serial.print("Failed to connect with state: ");
      Serial.print(client.state());
      delay(2000);
    }
  }

  // Publish that we've connected to the MQTT Broker
  client.publish(clientID, "On & Connected");

  // Subscribe to devices topic
  client.subscribe(clientID);

  // Print MAC Addresses
  Serial.println("MAC Address: ");
  Serial.println(WiFi.macAddress());
  testLights();
}
