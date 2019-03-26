#include <OneWire.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define ONE_WIRE_BUS 2

const char* ssid     = "Asgard";
const char* password = "5925362000";


float get_data() {
    OneWire ds(ONE_WIRE_BUS);

    byte data[12];
    byte addr[8];

    Serial.print("Connecting to sensor.");

    if (!ds.search(addr)) {
        Serial.println("No more addresses.");
        while(1);
    }
    ds.reset_search();

    if (OneWire::crc8(addr, 7) != addr[7]) {
        Serial.println("CRC is not valid.");
        while(1);
    }

    ds.reset();
    ds.select(addr);
    ds.write(0x44);
    delay(1000);

    ds.reset();
    ds.select(addr);
    ds.write(0xBE);

    Serial.print("Reading temperature.");

    for (int i = 0; i < 9; i++) {
        data[i] = ds.read();
    }

    int raw = (data[1] << 8) | data[0];
    if (data[7] == 0x10) raw = (raw & 0xFFF0) + 12 - data[6];

    return raw / 16.0;
}

void send_data(float temp) {
    HTTPClient http;

    byte addr[6];
    char* addr_str = "%02X:%02X:%02X:%02X:%02X:%02X";
    char* host = "http://192.168.100.112/api?temp=%s&addr=%s";
    char* temp_str;

    sprintf(temp_str, "%f", temp);

    WiFi.macAddress(addr);
    sprintf(addr_str, "%s", addr[0], addr[1], addr[2], addr[3], addr[4], addr[5]);

    Serial.print("Connecting to Wi-Fi.");

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.print("Sending temp: ");
    Serial.println(temp_str);
    Serial.print(" and address: ");
    Serial.println(addr_str);

    sprintf(host, temp_str, addr_str);
    http.begin(host);

    http.GET();
    http.end();
}


void setup() {
    float temp;

    Serial.begin(115200);
    Serial.setTimeout(2000);

    while (!Serial) { }

    // temp = get_data();
    // send_data(temp);

    // Serial.println("Entering to deep sleep.");
    // ESP.deepSleep(18e8);
}


void loop() {
    float temp;

    // Debug mode
    temp = 20.0;
    send_data(temp);
    delay(10000);
}