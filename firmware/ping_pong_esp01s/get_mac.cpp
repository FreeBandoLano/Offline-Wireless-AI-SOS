/*
 * Quick MAC Address Discovery Sketch
 * 
 * Flash this to both ESP8266 boards first to get their MAC addresses.
 * Then update the main ping-pong firmware with correct PEER_MAC values.
 * 
 * Upload this, open Serial Monitor (115200 baud), note MAC addresses,
 * then flash the main ping-pong firmware with updated MAC values.
 */

#include <ESP8266WiFi.h>

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n=== ESP8266 MAC Address Discovery ===");
  
  WiFi.mode(WIFI_STA);
  
  String mac = WiFi.macAddress();
  Serial.print("MAC Address: ");
  Serial.println(mac);
  
  // Print in array format for easy copy-paste
  Serial.print("For firmware PEER_MAC[]: {");
  mac.replace(":", ",0x");
  mac = "0x" + mac;
  Serial.print(mac);
  Serial.println("}");
  
  Serial.println("\nCopy this MAC address to the OTHER board's PEER_MAC[] array");
  Serial.println("=== Discovery Complete ===\n");
}

void loop() {
  // Blink built-in LED to show it's running
  digitalWrite(LED_BUILTIN, LOW);   // LED on
  delay(500);
  digitalWrite(LED_BUILTIN, HIGH);  // LED off  
  delay(500);
}