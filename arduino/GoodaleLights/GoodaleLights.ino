#include "Arduino.h"
#include <Ethernet.h>
#include <SPI.h>

byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0x74, 0x34 };

// Enter the IP address of the server you're connecting to:
IPAddress server(18, 189, 16, 206); 

// Initialize the Ethernet client library
// with the IP address and port of the server 
// that you want to connect to (port 23 is default for telnet;
// if you're using Processing's ChatServer, use  port 10002):
EthernetClient client;

void setup() {
  Serial.begin(9600);
  Ethernet.begin(mac);

  // give the Ethernet shield a second to initialize:
  delay(3000);
  Serial.println("connecting...");

  // if you get a connection, report back via serial:
  if (client.connect(server, 8123)) {
    Serial.println("connected");
  } 
  else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
}

void loop() {
  // if there are incoming bytes available 
  // from the server, read them and print them:
  
  String inMessage = "";
  while (client.available()) {
    char c = client.read();
    inMessage += c;
  }
  
  if (inMessage.length() > 0) {
    Serial.print(inMessage);
  }

  if (inMessage.indexOf("Name?") >= 0) {
    delay(1000);
    client.println("goodale");
    Serial.println("Registered as goodale");
  }

  // if the server's disconnected, stop the client:
  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
    // do nothing:
    while(true);
  }
}
