/*
* Arduino Wireless Communication Tutorial
*     Example 1 - Transmitter Code
*
* by Dejan Nedelkovski, www.HowToMechatronics.com
*
* Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
*/

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8);  // CE, CSN

const byte address[6] = "00001";

void setup() {
    Serial.begin(115200);
    radio.begin();
    radio.openWritingPipe(address);
    radio.setPALevel(RF24_PA_HIGH);
    radio.setDataRate(RF24_2MBPS);
    radio.setPayloadSize(200);
    radio.setAutoAck(true);
    radio.stopListening();
}

struct pck {
    char element = 0;
};

pck data;

void loop() {

    if (Serial.available() > 0) {
        // Read the incoming byte
        data.element = Serial.read();

        // Print the incoming byte to the serial terminal
        //Serial.print(incomingByte);
        //Serial.print(data.element);
        radio.write(&data, sizeof(data));
    }
}