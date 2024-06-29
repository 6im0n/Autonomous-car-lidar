/*
this program taken from arduino Example .
  modified by By Mohannad Rawashdeh
  http://www.genotronex.com
  This code used to control the digital potentiometer
  MCP41100 connected to  arduino Board
  CS >>> D10
  SCLK >> D13
  DI  >>> D11
  PA0 TO VCC
  PBO TO GND
  PW0 TO led with resistor 100ohm .
*/
#include <SPI.h>
byte address=0x11;
int CS= 10;

void setup()
{
  pinMode (CS, OUTPUT);
  SPI.begin();
  Serial.begin(9600);
  Serial.print("init start\n");
  digitalPotWrite(125);
  delay(5000);
  Serial.print("init end\n");
}

void loop()
{
  digitalPotWrite(125);
    for (int i = 90; i <= 160; i++)
    {
      digitalPotWrite(i);
      Serial.print(i);
      Serial.print("\n");
      delay(50);
    }
    delay(1000);
    for (int i = 160; i >= 90; i--)
    {
      digitalPotWrite(i);
      Serial.print(i);
      Serial.print("\n");
      delay(50);
    }

}

int digitalPotWrite(int value)
{
  digitalWrite(CS, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(CS, HIGH);
}
