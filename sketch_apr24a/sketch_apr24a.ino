#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <HTTPClient.h> 
#include <ArduinoJson.h>

const char* ssid = "MIP";
const char* password = "11333356";
const char* serverUrl = "http://192.168.174.1:3000/api/button"; // Ubah dengan URL API Anda
const int buttonPin = 2; // Pin untuk tombol fisik

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP); // Aktifkan pull-up internal
  WiFi.begin(ssid, password); // Mulai koneksi WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  int buttonState = digitalRead(buttonPin);
  if (buttonState == LOW) {
    Serial.println("Tombol ditekan!");
    sendDataToAPI();
    delay(1000); // Hindari pengiriman berkali-kali dalam satu detik
  }
}

void sendDataToAPI() {
  // Persiapkan data untuk dikirim ke API
  DynamicJsonDocument jsonBuffer(200);
  jsonBuffer["buttonState"] = "pressed";

  // Buat objek HTTPClient
  HTTPClient http;

  // Kirim POST request ke API
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonBuffer.as<String>());
  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.println("Error sending POST request");
  }
  http.end();
}
