#include <DHT.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define DHTTTHRESHOLD 11

#define SERVER_ADDRESS "http://192.168.0.103"
#define SENSOR_ID "CXX"

#define SSID "WiFi SSID"
#define PSWD "WiFi Password"

/***
  For working with a faster than ATmega328p 16 MHz chip, like an ESP8266,
  you need to increase the threshold for cycle counts.
  You can do this by passing a 3rd parameter for this threshold.
  11 - is good for the ESP8266 processor on ESP-01.
***/
DHT dht(DHTPIN, DHTTYPE);


void setup() {
  Serial.begin(115200);

  Serial.println();
  Serial.print("[WIFI] Connecting to ");
  Serial.println(SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PSWD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("[WIFI] Connected");
  Serial.println("[WIFI] IP address: ");
  Serial.println(WiFi.localIP());

  Serial.println("[DHT] Begin connection");
  dht.begin();
}

void loop() {

  if ((WiFi.status() == WL_CONNECTED)) {
    float temp = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temp) || isnan(humidity)) {
      Serial.println("[DHT] Failed to read the data");
    } else {
      WiFiClient client;
      HTTPClient http;

      Serial.println("[HTTP] Begin request");
      http.begin(client, SERVER_ADDRESS);
      http.addHeader("Content-Type", "application/json");

      String payload = String("{\"sensor_id\":\"") + SENSOR_ID +
                       String("\",\"temp\":") + temp +
                       String(",\"humidity\":") + humidity + String("}");
      int httpCode = http.POST(payload);
      if (httpCode > 0) {
        if (httpCode == HTTP_CODE_OK) {
          const String& payload = http.getString();
          Serial.println("[HTTP] Response:\n<<");
          Serial.println(payload);
          Serial.println(">>");
        } else {
          Serial.printf("[HTTP] Error: %s\n", http.errorToString(httpCode).c_str());
        }
      }

      http.end();
    }
  }

  delay(5 * 60 * 1000);
}
