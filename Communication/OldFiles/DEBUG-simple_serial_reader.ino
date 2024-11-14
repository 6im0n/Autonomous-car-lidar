void setup() {
  // Initialize serial communication at 9600 bits per second
  Serial.begin(115200);
}

void loop() {
  // Check if data is available to read from the serial port
  if (Serial.available() > 0) {
    // Read the incoming byte
    char incomingByte = Serial.read();

    // Print the incoming byte to the serial terminal
    Serial.print(incomingByte);
  }
}
