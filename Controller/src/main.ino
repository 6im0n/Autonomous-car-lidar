struct Command {
    const char* name;
    void (*function)(int values);
};

enum Direction {
    LEFT,
    RIGHT
};

void turnWheel(int values)
{
    if (values == LEFT) {
    } else {
    }

}

void moveForward(int values)
{
}

void moveBackward(int values)
{
}

void stop(int values)
{
}

Command commands[] = {
        {"WHEELS_DIR", turnWheel},
        {"CAR_FORWARD", moveForward},
        {"CAR_BACKWARDS", moveBackward},
        {"STOP_SIMULATION", stop}
};

void setup() {
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil(':');
        int values = Serial.parseInt();

        for (int i = 0; i < sizeof(commands) / sizeof(Command); i++) {
            if (command == commands[i].name) {
                commands[i].function(values);
                break;
            }
        }
    }
}
