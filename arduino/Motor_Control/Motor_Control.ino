
//-------------------------------모터부--------------------------------

//조향
const int pin_FR = 26;        // LOW : CW, HIGH : CCW
const int pin_RS = 28;        // LOW : Run, HIGH : Stop
const int pin_Brk = 27;       // LOW : Free, HIGH : Brake
const int SPEED = 8;

const int pin_FR_brk = 30;        // LOW : CW, HIGH : CCW
const int pin_RS_brk = 31;        // LOW : Run, HIGH : Stop
const int pin_Brk_brk = 32;       // LOW : Free, HIGH : Brake
const int SPEED_brk = 9;


//모터 제어
int motorspeed = 0;
int alarm = 0;
int count = 0;
boolean doBrake = false;
boolean UpDown = true;
int value = 0;
int state = 0;
int prevState = 0;
int lineOutValue = 500;
bool trig_brk=false;
//엔코더
int pinA = 2;
int pinB = 3;
int encoderPosCount = 0;
int pinALast;
int aVal;
boolean bCW;
int maxValue = 66;

// 통신부
String inString = "";
int angle, distance = 0;
boolean minus = false;
char buffer[20];
char bufferIndex = 0;

void updateEncoderValue();
void steer();

void setup() {
  Serial.begin(115200);
  Serial.flush();
  Serial.println(">> ");

  //조향
  pinMode(pin_FR, OUTPUT);
  pinMode(pin_RS, OUTPUT);
  pinMode(pin_Brk, OUTPUT);

  //브레이크
  pinMode(pin_FR_brk, OUTPUT);
  pinMode(pin_RS_brk, OUTPUT);
  pinMode(pin_Brk_brk, OUTPUT);

  //엔코더
  pinMode(pinA, INPUT);
  pinMode(pinB, INPUT);

  pinALast = digitalRead(pinA);

  //인터럽트 시작
  attachInterrupt(digitalPinToInterrupt(pinA), updateEncoderValue, CHANGE);
  attachInterrupt(digitalPinToInterrupt(pinB), updateEncoderValue, CHANGE);

  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);

}


void loop() {
  delay(50);

  //----------------------------------------통신부------------------------------------------------------
  while (Serial.available() > 0) {

    buffer[bufferIndex] = Serial.read();
    //Serial.println(buffer[bufferIndex]);
    char inChar = (buffer[bufferIndex]);
    //Serial.println(inChar);
    bufferIndex++;
    bufferIndex = bufferIndex % 20;

    //int inChar = Serial.read();

    if ('0' <= inChar && inChar <= '9') {
      // convert the incoming byte to a char
      // and add it to the string:
      inString += (char)inChar;
    }

    else {
      char  c = (char)inChar;
      if (c == 'a') {
        angle = inString.toInt();
        inString = "";
      }
      else if (c == 'd') {
        distance = inString.toInt();
        inString = "";
        doBrake = false;
      }
      else if (c == '-') {
        minus = true;
      }
      else if (c == 's') {
        doBrake = true;
      }
    }

  }

  if (minus) {
    distance *= -1;
    minus = false;
  }


  //----------------------------------------------------------------------------------------------------

  //-------------------------------------------모터 제어부----------------------------------------------

  //Serial.println(distance);
  // case 1 : Distance > 0 && angle < 90      Rear
  // case 2 : distance < 0 && angle > 90      Forward
  // case 3 : distacne > 0 && angle > 90      Forward
  // case 4 : distance < 0 && angle < 90      Rear

  // 현재 상태 case 분류
  if (-300 < distance && distance <= -140) state = -3;
  if (-140 < distance && distance <= -80) state = -2;
  if (-80 < distance && distance <= -30) state = -1;
  if (-30 < distance && distance <= 30) state = 0;
  if (30 < distance && distance <= 80) state = 1;
  if (80 < distance && distance <= 140) state = 2;
  if (140 < distance && distance <= 300) state = 3;


  if (doBrake == true && trig_brk==false /*|| abs(distance) > lineOutValue*/) { // 정지선 검출 or 주행 중 코스 이탈
    //조향을 푼다
      // CW
    digitalWrite(pin_FR_brk, LOW);
    digitalWrite(pin_Brk_brk, LOW);
    digitalWrite(pin_RS_brk, LOW);  // Low : Run
  
    // 민감도 중간
    analogWrite(SPEED_brk, 100);    // 100, 150 
    delay(2000);                // 1000
    digitalWrite(pin_RS_brk, HIGH); // High : Stop
    delay(1000);
    
    // CCW
    digitalWrite(pin_FR_brk, HIGH);  // High : CCW
    digitalWrite(pin_Brk_brk, LOW); // Low : Free
    digitalWrite(pin_RS_brk, LOW);  // Low : Run
    
    analogWrite(SPEED_brk, 100);
    delay(2000);                // 3초 후에 모터 Stop
    digitalWrite(pin_RS_brk, HIGH); // High : Stop
    delay(20000);
    doBrake = false;

    trig_brk = true;
  }
  else if (state != prevState) {                                                // 일반 주행 상태일시 모터 작동
    steer();
  }
  prevState = state;
  //---------------------------------------------------------------------------------------------------------
}


void runMotor(int dir, int delayTime) {
  //delay(1000);                                            ][          도열이 확인 가능하게 ! 1초 뒤 구동
  //dir 방향으로 delayTime만큼 돌리고
  digitalWrite(pin_FR, dir);
  digitalWrite(pin_Brk, LOW);
  digitalWrite(pin_RS, LOW);                // LOW = START
  analogWrite(SPEED, 100);                                                                                                           //값 결정
  delay(delayTime);

  //모터 정지
  //digitalWrite(pin_RS, HIGH);               // HIGH = STOP
  analogWrite(SPEED, 0);                                                                                                           //값 결정
}

void steer() {

  int rot, val1, val2;
  bool left;    //
  bool right;   //
  val1 = 50;   //LOW값
  val2 = 100;   //HIGH값

  if (abs(state - prevState) > 2) digitalWrite(13, HIGH);   // 튀는 값 확인

  if (state - prevState > 0) rot = HIGH;      // high :  왼->오
  else if (state - prevState < 0) rot = LOW;  // log : 오->왼
  switch (state) {
    case -3:
      runMotor(LOW, 600);    // high 반시계(좌회전) -> val2, low 시계(우회전) -> val1
      break;
    case -2:
      if (rot == HIGH) runMotor(HIGH, 600);
      else if (rot == LOW) runMotor(LOW, 600);
      break;
    case -1:
      if (rot == HIGH) runMotor(HIGH, 600);
      else if (rot == LOW) runMotor(LOW, 600);
      break;
    case 0:
      if (rot == HIGH) runMotor(HIGH, 600);
      else if (rot == LOW) runMotor(LOW, 600);
      break;
    case 1:
      if (rot == HIGH) runMotor(HIGH, 600);
      else if (rot == LOW) runMotor(LOW, 600);
      break;
    case 2:
      if (rot == HIGH) runMotor(HIGH, 600);
      else if (rot == LOW) runMotor(LOW, 600);
      break;
    case 3:
      runMotor(HIGH, 600);
      break;

  }
}

void updateEncoderValue() {

  Serial.print("encoder value : ");
  Serial.println(encoderPosCount);
  
  if (abs(encoderPosCount) > 200) {
    digitalWrite(pin_RS, LOW);  //모터 정지
    digitalWrite(13, HIGH);
  }
  aVal = digitalRead(pinA);
  if (aVal != pinALast) {
    if (digitalRead(pinB) != aVal) {
      encoderPosCount++;
      bCW = true;
    }
    else {
      bCW = false;
      encoderPosCount--;
    }
  }
  pinALast = aVal;
}
