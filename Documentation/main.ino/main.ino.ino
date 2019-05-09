#include <Servo.h>
#include <Wire.h>

//I2C config
#define SLAVE_ADDRESS 0x12
int dataReceived = 0;

//Servo config
#define SERVO_MIN_ANGLE 0
#define SERVO_MAX_ANGLE 45
int servoPin[] = {2, 3, 4 ,5 ,6 ,7};
Servo servo[6];
int servoState[6]= {0, 0, 0, 0, 0, 0};

void setup() {
    Serial.begin(9600);
    Wire.begin(SLAVE_ADDRESS);
    //Set the callback function
    Wire.onReceive(receiveData);

    //Setup Servos with their respective pins
    for (int i = 0; i < 6; i++)
    {
      servo[i].attach(servoPin[i]);
      pinMode(servoPin[i], OUTPUT);
    }

    pinMode(10, OUTPUT);
    digitalWrite(10, HIGH);
}

void loop() {
    delay(100);
}

void moveServo(int i){
  if(servoState[i] < SERVO_MAX_ANGLE){
    servo[i].write(SERVO_MAX_ANGLE);
    servoState[i] = SERVO_MAX_ANGLE;
  }
  else {
    servo[i].write(SERVO_MIN_ANGLE);
    servoState[i] = SERVO_MIN_ANGLE;
  }
}

void receiveData(int byteCount){
    while(Wire.available()) {
        dataReceived = Wire.read();
        if (dataReceived >= 1 && dataReceived <= 6){
          moveServo(dataReceived - 1);
        }
        else{
          Serial.println("Error : wrong servo address");
        }
    }
}
