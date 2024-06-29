#include <WiFi.h>

// Set your access point credentials
const char *ssid = "CAR_WIFI";
const char *password = "Epitech4242";

// Set the TCP server port
const uint16_t serverPort = 4242;

WiFiServer server(serverPort);

void setup() {
  // Initialize serial communication
  Serial.begin(115200);

  // Set up the WiFi Access Point
  WiFi.softAP(ssid, password);
  Serial.println("Access Point Started");
  Serial.println(ssid);

  // Print the IP address
  Serial.print("IP Address: ");
  Serial.println(WiFi.softAPIP());

  // Start the TCP server
  server.begin();
  Serial.println("TCP server started");
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (client) {
    Serial.println("Client connected");

    // Read and send data as long as the client is connected
    while (client.connected()) {
      // Buffer to store incoming serial data
      uint8_t buffer[100];
      int bytesRead = 0;

      // Read data from the serial port if available
      while (Serial.available() > 0 && bytesRead < sizeof(buffer)) {
        buffer[bytesRead++] = Serial.read();
      }

      // Send the buffered data to the client
      if (bytesRead > 0) {
        client.write(buffer, bytesRead);
      }
    }

    // Client disconnected
    Serial.println("Client disconnected");
    client.stop();
  }
}
