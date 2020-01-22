#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* deviceID = "001";
const int R = 15;
const int G = 12;
const int B = 16;
 
const char* ssid = "yale wireless";             //
const char* password =  "";
const char* mqttServer = "farmer.cloudmqtt.com";    //35.239.98.209 for our python server    farmer.cloudmqtt.com for cloud mqtt
const int mqttPort = 14479;  
const char* mqttUser = "xoemllsy";     // yale for ours.    xoemllsy for cloud mqtt
const char* mqttPassword = "hdgazSRFNst3";    //lightsnstuff for ours,    hdgazSRFNst3 for cloudmqtt
 
WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {
 
  Serial.begin(115200);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {
 
      Serial.println("connected");  
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }

  client.publish(deviceID, "On & Connected");
  client.subscribe("To Chips");
  testLights();
  Serial.println(WiFi.macAddress());
 
}
 
void callback(char* topic, byte* data, unsigned int length) {
 
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
 
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)data[i]);
  }

  //find data
    bool getID = 0;
    bool getCommand = 0;
    String gotID = "";
    String command = "";
    for (int i=0; i < length; i++)
    {
      if ((char)data[i] ==')' && getCommand){
        getCommand = 0;
        //Serial.println(command);
        changeColors(command);
        break;}
      
      if (getCommand){
        command+=(char)data[i];}
      
      if ((char)data[i] =='.'){
        command = "";
    //    Serial.println(gotID);
        getID = 0;
        if (gotID == deviceID){
          getCommand=1;}}
      
      if (getID){
        gotID+=(char)data[i];}

      if (((char)data[i])=='('){
        gotID = "";
        getID = 1;}

    }
  
 
  Serial.println();
  Serial.println("-----------------------");
 
}
 
void loop() {
  client.loop();
}

void changeColors(String command){
  String r = "";
  r += command.charAt(0); 
  r += command.charAt(1);
  r += command.charAt(2);
  String g = "";
  g += command.charAt(4); 
  g += command.charAt(5);
  g += command.charAt(6);
  String b = "";
  b += command.charAt(8); 
  b += command.charAt(9);
  b += command.charAt(10);

  Serial.println(r);
  Serial.println(g);
  Serial.println(b);
  
  
  analogWrite(R, (abs (r.toInt() - 255)));
  analogWrite(G, (abs (g.toInt() - 255)));
  analogWrite(B, (abs (b.toInt() - 255)));

}

void testLights(){
    analogWriteRange(255);
    pinMode(R, OUTPUT);
    pinMode(G, OUTPUT);
    pinMode(B, OUTPUT);
    
    analogWrite(R, 255);
    analogWrite(G, 255);
    analogWrite(B, 255);
    
    delay(100);
    
    
    analogWrite(R, 0);
    delay(500);
    analogWrite(R, 255);
    analogWrite(G, 0);
    delay(500);
    analogWrite(G, 255);
    analogWrite(B, 0);
    delay(500);
    analogWrite(B, 255);
}
