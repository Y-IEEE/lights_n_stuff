#include <ESP8266WiFi.h>
#include <PubSubClient.h>

/*
* DEVICE MAC ADDRESS: 
*/

/*
* IDENTIFICATION INFORMATION:
*/
const int identificationNum = 1;
const char* clientID = "00" + identificationNum;
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
const int R_pin = 15;
const int G_pin = 12;
const int B_pin = 16;

WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {

  Serial.begin(115200);
 
  // Loop until wifi connection succeeds
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
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
  // client.publish(clientID, "On & Connected");

  // Subscribe to devices topic
  client.subscribe(clientID);

  // Print MAC Addresses
  Serial.println("MAC Address: ");
  Serial.println(WiFi.macAddress());
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
}

/*
* Convert string of form "255/255/255" to individual RGB values and turn on lights
*/
void changeColors(char* colorString) {
  // Set up light pins
  analogWriteRange(255);
  pinMode(R_pin, OUTPUT);
  pinMode(G_pin, OUTPUT);
  pinMode(B_pin, OUTPUT);

  // Tokenize (split) each string into individual color values
  char * red_value;
  char * green_value;
  char * blue_value;

  red_value = strtok(colorString, "/");
  green_value = strtok(colorString, "/");
  blue_value = strtok(colorString, "/");

  // log the values
  Serial.println(red_value);
  Serial.println(green_value);
  Serial.println(blue_value);
  
  // Turn on the lights
  analogWrite(R_pin, (abs (atoi(red_value) - 255)));
  analogWrite(G_pin, (abs (atoi(green_value) - 255)));
  analogWrite(B_pin, (abs (atoi(blue_value) - 255)));
}
