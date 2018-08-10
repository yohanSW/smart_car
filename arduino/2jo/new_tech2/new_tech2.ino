int PUL=6; //define Pulse pin
int DIR=4; //define Direction pin
int ENA=2; //define Enable Pin

float Xdata;
float Ydata;
float Zdata;

bool step_DIR;
int step_MOVE;

void setup() {
  pinMode (PUL, OUTPUT);
  pinMode (DIR, OUTPUT);
  pinMode (ENA, OUTPUT);
}

void loop() 
{
  Serial.println('G');
  get_data();
  
  /* Change Sensor data into Step Motor degree. In Step Motor, Use Ydata */
  if(Ydata >= 0)
  {
    step_DIR = true;
    step_MOVE = int(Ydata * 100);
  }
  else
  {
    step_DIR = false;
    Ydata = -Ydata;
    step_MOVE = int(Ydata * 100);
  }
  
  for (int i=0; i<step_MOVE; i++)    //950이 한바꾸
  {
    digitalWrite(DIR,step_DIR);
    digitalWrite(ENA,LOW);
    digitalWrite(PUL,HIGH);
    delayMicroseconds(500);
    digitalWrite(PUL,LOW);
    delayMicroseconds(500);
  }
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
        Xdata = Serial.parseFloat();
        Ydata = Serial.parseFloat();
        Zdata = Serial.parseFloat();
      }
      else
        continue;
      break;
    }
    else
      continue;
  }
}


