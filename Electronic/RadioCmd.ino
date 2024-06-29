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
int car_power = 9;
int wheels_dir = 10;


struct car_data_s {
  float forward = -42.0;
  float backward = -42.0;
  float dir = -42.0;
};

struct car_command_s{
  int pow = 125;
  int dir = 125;
};

car_command_s car_command;

car_data_s car_data;

void setup()
{
  pinMode (car_power, OUTPUT);
  pinMode (wheels_dir, OUTPUT);
  pinMode (13, OUTPUT); //led
  SPI.begin();
  Serial.begin(9600);
  Serial.print("init start\n");
  Serial.println("Please start the radio transmitter");
  Serial.println("You have 5 sec to start it");
  initRadio();
  Serial.print("init end\n");
  init_value();
}

void initRadio(void)
{
  for(int i = 0; i < 50; i++)
  {
    carPowerWrite(125);
    wheelsDirWrite(125);
    delay(100);

  }

  carPowerWrite(0); // learn to the radio the min of the potentiometter
  delay(50);
  carPowerWrite(125); // back to "0"
  delay(50);
  carPowerWrite(255); // learn to the radio the max value of the potentiometter
  delay(50);
  carPowerWrite(125); // back to "0"

  wheelsDirWrite(0); // learn to the radio the min of the potentiometter
  delay(25);
  wheelsDirWrite(125); // back to "0"
  delay(25);
  wheelsDirWrite(255); // learn to the radio the max value of the potentiometter
  delay(25);
  wheelsDirWrite(125); // back to "0"
}


void parseString(String str) {
  // Check for CAR_FORWARD
  if (str.startsWith("CAR_FORWARD:")) {
    String valueStr = str.substring(12);
    car_data.forward = valueStr.toFloat();
    return;
  }
  // Check for CAR_BACKWARDS
  if (str.startsWith("CAR_BACKWARDS:")){
    String valueStr = str.substring(14);
    car_data.backward = valueStr.toFloat();
    return;
  }
  // Check for CAR_WHEELS
  else if (str.startsWith("WHEELS_DIR:")) {
    String valueStr = str.substring(11);
    car_data.dir = valueStr.toFloat();
    return;
  }
}

void reset_data(void)
{
  car_data.forward = -42.0;
  car_data.backward = -42.0;
  car_data.dir = -42.0;
}

void init_value(void)
{
  car_data.forward = -42.0;
  car_data.backward = -42.0;
  car_data.dir = -42.0;

  car_command.pow = 125;
  car_command.dir = 125;
}

void check_value(void)
{
  if (car_data.forward == -42.0 && car_data.backward == -42.0)
    car_command.pow = 125;
  if (car_data.dir == -42.0)
    car_command.dir = 125;
}

// value to send is between 0 and 125 for forward and
// value between 125 and 255 for backward
void car_send(void)
{
  if (car_data.dir != -42.0) {
    if (car_data.dir >= -1 && car_data.dir <= 0.0)
    {
      car_command.dir = 125 - (125 * car_data.dir);
    }
    else if (car_data.dir > 0.0 && car_data.dir <= 1.0)
    {
      car_command.dir = 125 - (125 * car_data.dir);
    }
  }
  if (car_data.forward != -42.0) {
    if (car_data.forward >= 0.0 && car_data.forward <= 1.0)
    {
      car_command.pow = 70 - (70 * car_data.forward);
      car_data.forward == 0.0 ? car_command.pow = 125 : 0;
      car_command.pow < 50 ? car_command.pow = 50 : 0;
    }
  }
  if (car_data.backward != -42.0) {
    if (car_data.backward >= 0.0 && car_data.backward <= 1.0)
    {
      if(car_command.pow < 125){
        carPowerWrite(200);
        delay(200);
        carPowerWrite(125);
        delay(200);
        carPowerWrite(200);
        delay(200);
        carPowerWrite(125);
      }
      car_command.pow = 210 + (45 * car_data.backward);
      car_data.backward == 0.0 ? car_command.pow = 125 : 0;
      //car_command.pow > 230 ? car_command.pow = 230 : 0;
    }
  }
}

void loop()
{
  reset_data();
  if (Serial.available() > 0) {
    String string_to_parse = Serial.readStringUntil('\n');
    parseString(string_to_parse);
    car_send();

    carPowerWrite(125);
    carPowerWrite(car_command.pow);
    wheelsDirWrite(125);
    wheelsDirWrite(car_command.dir);

    //Serial.println(car_data.forward);
    //Serial.println(car_data.backward);
    Serial.println(car_data.dir);
    Serial.println(car_command.dir);
  }
}


int carPowerWrite(int value)
{
  digitalWrite(car_power, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(car_power, HIGH);
}

int wheelsDirWrite(int value)
{
  digitalWrite(wheels_dir, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(wheels_dir, HIGH);
}
