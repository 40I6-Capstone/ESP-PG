#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
//#include <WebSocketsClient.h>

WiFiClient client;

const unsigned long duration = 5000;
unsigned long timeLatestCycle = 0;
boolean ledStatus;

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

char state;

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

  state = 'I'; // set to idle state by default
        
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

  /*
  FSM Definitions:
  C - CONNECT STATE
  I - IDLE STATE
  S - SEND STATE
  A - PATH ALLOCATION STATE
  P - PATH RECEIVE STATE
  R - RESPOND_CHECK STATE
  */

  // FSM
  switch (state){

    case 'I': // IDLE STATE
      Serial.printf("[FSM] IDLE STATE \n");
      if(strcmp(getMessage(4),"node")==0){
        state = 'S'; // go to send_state
        break;
      }
        
      else if(strcmp(getMessage(4),"path")==0){
        state = 'A'; //go to path allocation state
        break;
      }

    case 'S': // SEND STATE
      Serial.printf("[FSM] SEND STATE \n");
      // TODO - add tx code to send current state to server
      state = 'I'; // go back to idle state
      break;

    case 'A': // PATH ALLOCATION STATE
      Serial.printf("[FSM] PATH ALLOCATION STATE \n");
      // TODO - send 'ready' to server
      state = 'P'; // go to path receive state
      break;

    case 'P': // PATH RECEIVE STATE
      Serial.printf("[FSM] PATH RECEIVE STATE \n");
      char* packet;
      packet = getMessage(40);
      // TODO - add code for converting received data 
      state = 'R'; // go to respond check state
      break;

    case 'R': // RESPOND_CHECK STATE
      Serial.printf("[FSM] RESPOND_CHECK STATE \n");
      if(strcmp(getMessage(4),"good")==0){
        state = 'I'; // go back to idle
        break;
      }
        
      else if(strcmp(getMessage(4),"nope")==0){
        state = 'A'; //go back to allocation state
        break;
      }
      
      state = 'I'; // default state is idle
      break;

  }

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

    return buffer;
}

// TODO - write a convert data function
