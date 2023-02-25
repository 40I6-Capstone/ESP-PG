#include <Arduino.h>
//#include <WiFi.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>

//const char* ssid = "";
//const char* password = "";
//const char* server_ip = "";
//const int server_port = 1234;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  WiFi.begin("", "");

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("WiFi connected");
  Serial.println("Connecting to server...");

  if (!client.connect("", 1234)) {
    Serial.println("Connection failed");
    return;
  }

  Serial.println("Connected to server");
}

void loop() {
  // Send a message to the server
  client.print("Hello from ESP32 or ESP8266");

  // Wait for the server to respond
  while (client.available()) {
    char c = client.read();
    Serial.write(c);
  }

  delay(1000);
}
