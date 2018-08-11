#include <Servo.h>

Servo Xservo;

int PUL=6; //define Pulse pin
int DIR=4; //define Direction pin
int ENA=2; //define Enable Pin
int SERVO = 5; //define Servo Pin

/* Sensor data */
float Xdata=0;
float Ydata=0;
float Zdata=0;

/* Step Motor */
bool step_DIR;
int step_MOVE;

/* Servo Motor */
int servo_MOVE;

void setup() 
{
  pinMode (PUL, OUTPUT);
  pinMode (DIR, OUTPUT);
  pinMode (ENA, OUTPUT);
  Xservo.attach(SERVO);
  Xservo.write(45); // servo motor must be started at 45 degree
  servo_MOVE = 45;
  Serial.begin(115200);
}

void loop() 
{
  get_data();

  /* Change Sensor data into Servo Motor degree. In Servo Motor, Use Xdata */
  servo_MOVE += int(Xdata * 10);
  
  if(servo_MOVE <= 0)
  {
    servo_MOVE = 0;
  }
  else if(servo_MOVE >= 90)
  {
    servo_MOVE = 90;
  }
  
  /* Change Sensor data into Step Motor degree. In Step Motor, Use Ydata */
  if(Ydata >= 0)
  {
    step_DIR = HIGH;
    step_MOVE = int(Ydata * 20);
  }
  else
  {
    step_DIR = LOW;
    Ydata = -Ydata;
    step_MOVE = int(Ydata * 20);
  }
  /* Motor control by using MOVE data */


  
  for (int i=0; i<step_MOVE; i++)    //950 is 360 degree
  {
    digitalWrite(DIR,step_DIR);
    digitalWrite(ENA,LOW);
    digitalWrite(PUL,HIGH);
    delayMicroseconds(500);
    digitalWrite(PUL,LOW);
    delayMicroseconds(500);
    Xservo.write(servo_MOVE); // to control step motor and servo motor simultaneously, put servo.write into the for loop
  }
  Xdata=0;
  Ydata=0;
  Zdata=0;


}

void get_data()
{
    /* 입력가능한 불가능한 상태일 경우, while문 무한루프. 즉, 대기상태 */
  while(true) 
  {
    if(Serial.available())
    {
      if(Serial.find('#'))
      {
        Xdata += Serial.parseFloat();
        Ydata += Serial.parseFloat();
        Zdata += Serial.parseFloat();
      }
      else
        continue;
      break;
    }
    else
      continue;
  }
}

