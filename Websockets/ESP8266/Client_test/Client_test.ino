#include <Arduino.h>
//#include <WiFi.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>

//const char* ssid = "";
//const char* password = "";
//const char* server_ip = "";
//const int server_port = 1234;

WiFiClient client;

int i=0;
char buffer[6];

void getMessage(int len){
//    char buffer[len];

    if(client.available()){
       while(i<(len-1)){
          char c = client.read();
          buffer[i] = c;
          i++;
       }
       i=0;
       Serial.println(buffer);
    }

//    return buffer;
}

void setup() {
  Serial.begin(115200);

  for(uint8_t t = 3; t > 0; t--) { //wait 3 seconds to begin connection & transmission
    Serial.printf("[SETUP] BOOT WAIT %d...\n", t);
    Serial.flush(); //Waits for the transmission of outgoing serial data to complete
    delay(1000);
  }
  WiFi.persistent(false); // do not allow wifi configuration to persist in flash memory
  WiFi.begin();

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("WiFi connected");
  Serial.println("Connecting to server...");

  if (!client.connect("192.168.2.23", 1234)) {
    Serial.println("Connection failed");
    return;
  }

  Serial.println("Connected to server");
}

void loop() {
  // Send a message to the server
  client.print("Hello from ESP8266");

  getMessage(6);
  String test = buffer;
  Serial.print(test);
//
  if(test.compareTo("Hello")==0){
    Serial.print("Success");
  }
  
  // Wait for the server to respond
//  if(strcmp(test,"Hello")==0){
//    Serial.print("Success");
//  }
//  while (client.available()) {
//    char c = client.read();
//    Serial.write(c);
//  }

  delay(1000);
}
