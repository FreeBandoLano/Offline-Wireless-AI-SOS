#include <ESP8266WiFi.h>
#include <espnow.h>

#define ROLE_PINGER  1      // set to 0 on the “pong” board
#define JSON_BUF     128
uint8_t PEER_MAC[] = {0xAA,0xBB,0xCC,0xDD,0xEE,0xFF};   // fill with other board’s MAC

volatile bool gotPong = false;
volatile uint32_t sendMicros = 0, rttMicros = 0;
uint32_t seq = 0;

void onRecv(uint8_t *mac, uint8_t *data, uint8_t len) {
  if (ROLE_PINGER == 1) {
    // Incoming pong: compute RTT (μs)
    rttMicros = micros() - sendMicros;
    gotPong   = true;
  } else {
    // We are the pong board → echo straight back
    esp_now_send(mac, data, len);
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  if (esp_now_init() != 0) {
    Serial.println(F("ESP-NOW init failed")); return;
  }
  esp_now_set_self_role(ESP_NOW_ROLE_COMBO);
  esp_now_register_recv_cb(onRecv);

  // Add peer (needed only on the pinger)
  esp_now_add_peer(PEER_MAC, ESP_NOW_ROLE_COMBO, 1, NULL, 0);
}

void loop() {
#if ROLE_PINGER
  uint8_t payload[4];
  memcpy(payload, &seq, 4);

  sendMicros = micros();
  esp_now_send(PEER_MAC, payload, sizeof(payload));

  uint32_t tStart = millis();
  while (!gotPong && millis() - tStart < 1000) yield();   // 1 s timeout

  if (gotPong) {
    int32_t rssi = WiFi.RSSI();
    char j[JSON_BUF];
    snprintf(j, JSON_BUF,
      "{\"seq\":%lu,\"rssi\":%ld,\"lat_us\":%lu}", seq, rssi, rttMicros);
    Serial.println(j);
  } else {
    Serial.println(F("{\"error\":\"pong_timeout\"}"));
  }
  gotPong = false;
  seq++;
  delay(500);
#else
  delay(100);      // pong board idles
#endif
}
