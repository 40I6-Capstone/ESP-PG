#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
//#include <WebSocketsClient.h>

WiFiClient client;

const unsigned long duration = 5000;
unsigned long timeLatestCycle = 0;
boolean ledStatus;
char state = 'I';

const uint16_t port = 7890;
const char *host = "192.168.0.57";

//int data = 0;
int i = 0;

//  Example data for current node_state: (even though it is strings, when it is sent to the server, it is received as a byte array)
  String Heading = "30.64000";
  String Velocity = "5.145000";
  String X = "2.980000";
  String Y = "103.5000";
  String ts_ms = "10.00000";
  String State = "1";
  String data = Heading + Velocity + X + Y + ts_ms + State;
  //use client.print() to send a string to server


void setup() {
  Serial.begin(115200); //baud rate for serial communication

  Serial.setDebugOutput(true);
  delay(1000);
  Serial.println();
  pinMode(A0,INPUT);
 
  for(uint8_t t = 4; t > 0; t--) { //wait to begin connection & transmission
    Serial.printf("[SETUP] BOOT WAIT %d...\n", t);
    Serial.flush(); //Waits for the transmission of outgoing serial data to complete
    delay(1000);
  }

  Serial.printf("[SETUP] CONNECTING \n");
  WiFi.begin("COGECO-CD3A0", "DF9CECOGECO");
  
  while(WiFi.status() != WL_CONNECTED) { //wait until we are connected to the wifi
    delay(500);
    Serial.print(".");
  }
      
  Serial.printf("[SETUP] Connected to Wifi \n");
        
  state = 'I'; //Begin in idle state, "connect" state was built into setup()


}



char getMessage(int len){
    char buffer[len];
      
    char c = client.read();
      
    if(i<(len-1))
    {
      buffer[i] = c;
      i++;
    }
    
    if(i==(len-1)){
      Serial.println(buffer);
    }

    return *buffer;
}

void loop() {

//    check to make sure we are connected to the server otherwise wait and try again
  
    if (!client.connect(host, port))
    {
        Serial.println("Connection to host failed, Retrying...");
        delay(1000);
        return;
    }
    if (client){
      if(client.connected()){
        Serial.printf("Connected to Server \n");
      }
    }


    while(client.connected()){
      while(client.available()>0){
        Serial.write(client.read());
      }

    }
    if (client.available()) {
      Serial.println("Inside Client Available loop");
      char c = client.read();
      Serial.print(c);
    }


//    char test[] = {'n','o','d','e'};
//    client.write(test,4);
//    delay(3000);

  /*
  FSM Definitions:
  C - CONNECT STATE
  I - IDLE STATE
  S - SEND STATE
  A - PATH ALLOCATION STATE
  P - PATH RECEIVE STATE
  R - RESPOND_CHECK STATE
  */


    
//  switch (state){
//
//    case 'I':
//      Serial.printf("[FSM] IDLE STATE \n");
//      char buffer[4];
//      
//
//      char c = client.read();
//      
//      if(i<3)
//      {
//        buffer[i] = c;
//        i++;
//      }
//
//      Serial.println(buffer);
//      
////      while (client.available() > 0)
////      {
////          char c = client.read();
////          Serial.write(c);
////      }
////      
//      delay(7000);
//      state = 'S'; //move to SEND STATE
//      break;
//
//    case 'S':
//      Serial.printf("[FSM] SEND STATE \n");
//      state = 'A';
//      break;
//
//    case 'A':
//      Serial.printf("[FSM] PATH ALLOCATION STATE \n");
//      state = 'P';
//      break;
//
//    case 'P':
//      Serial.printf("[FSM] PATH RECEIVE STATE \n");
//
//      state = 'R';
//      break;
//
//    case 'R':
//      Serial.printf("[FSM] RESPOND_CHECK STATE \n");
//
//      state = 'I';
//      break;
//
//  }

}
