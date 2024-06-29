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
int CS= 9;
int last = 0;

void setup()
{
  pinMode (CS, OUTPUT);
  SPI.begin();
  Serial.begin(9600);
  Serial.print("init start\n");
  initRadio();
  Serial.print("init end\n");
}

void initRadio(void)
{
  for(int i = 0; i < 50; i++)
  {
    carPowerWrite(125);
    delay(100);

  }

  carPowerWrite(0); // learn to the radio the min of the potentiometter
  delay(50);
  carPowerWrite(125); // back to "0"
  delay(50);
  carPowerWrite(255); // learn to the radio the max value of the potentiometter
  delay(50);
  carPowerWrite(125); // back to "0"
}


void loop()
{
  int in = Serial.parseInt();

  if (in > 0 ){
    Serial.println(in);
    carPowerWrite(in);
  }
    // for (int i = 90; i <= 160; i++)
    // {
    //   digitalPotWrite(i);
    //   Serial.print(i);
    //   Serial.print("\n");
    //   delay(50);
    // }
    // delay(1000);
    // for (int i = 160; i >= 90; i--)
    // {
    //   digitalPotWrite(i);
    //   Serial.print(i);
    //   Serial.print("\n");
    //   delay(50);
    // }

}

int carPowerWrite(int value)
{
  digitalWrite(CS, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(CS, HIGH);
}
