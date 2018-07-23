#define clpin 4 // 엔코더, 클락핀
#define dtpin 11 // 엔코더, 데이타핀
#define swpin 12 //엔코더, 스위치핀
#define BRAKE 8 // 모터드라이버 -> 릴레이, LOW: Brake 해제 / HIGH: Brake
#define DIR 7 // 모터드라이버 -> 릴레이, LOW: CW / HIGH: CCW
#define SPEED 5 // 모터드라이버, PWM을 통한 모터 속도제어
#define gear_ratio 0.09 // 스티어링과 엔코더의 기어비 (58/25)*(15/360)


double steer_angle; // 회전시키고자 하는 스티어링 각도
double degree; // 회전시키고자 하는 엔코더 각도

/* Encoder Value 초기화 */
int encoderVal = 0; 
static int oldA = HIGH;
static int oldB = HIGH;

/* Serial 통신 초기화 */
long wheel_angle=0; // 조향각 (바퀴의 각도)
int minus_sig=1; // 조향각 (바퀴의 각도)
int is_break=0; // 차량 운행 정지 여부, 0: 운행 / 1: 정지


void setup() {
 pinMode (clpin, INPUT);
 pinMode (dtpin, INPUT);
 pinMode (swpin, INPUT);
 pinMode (BRAKE, OUTPUT);
 pinMode (SPEED, OUTPUT);
 pinMode (DIR, OUTPUT);
 digitalWrite (swpin, HIGH); // encoder 동작을 위한 switch ON
 digitalWrite (BRAKE, HIGH); // 데이터를 입력받기 전엔 모터는 정지상태로 시작
 Serial.begin(9600);
}

void loop() {

  /* 입력가능한 불가능한 상태일 경우, while문 무한루프. 즉, 대기상태 */
  while(true) 
  {
    if(Serial.available())
    {
      while(Serial.find('#'))
      {
        minus_sig = Serial.parseInt();
        wheel_angle=Serial.parseInt();
        if(minus_sig == 0)
          wheel_angle = -wheel_angle;
        is_break = Serial.parseInt();
      }
      break;
    }
    else{
     wheel_angle=-700;
  }


  
  /*
  if(wheel_angle != 0 && wheel_angle !=-700){
   Serial.print("wheel_angleValue=");
   Serial.println(wheel_angle);
   Serial.print("is break=");
   Serial.println(is_break);
  }
  */

  
  }
  
  steer_angle = wheel_angle * 13 ; // 스티어링 각도와 조향 각도의 비 13 : 1
  degree = steer_angle * gear_ratio;
  
  /* 엔코더 조향각이 바뀔 때마다 steer_angle입력을 막기 위해 while문 추가*/
  while(1)
  {
    int change = getEncoderTurn(); // encoder 각도 변화량
    encoderVal = encoderVal + change; // encoder 각도 갱신

    /* encoder 각도계산 종료시 초기화, 자율주행 종료시 switch OFF */
    if (digitalRead(swpin) == LOW)
    {
      encoderVal = 0;
    }
    
    Serial.println(encoderVal);
    
    digitalWrite(BRAKE,LOW); // 모터동작을 시작하기 위해 브레이크 해제
    
    if (encoderVal <= degree) // 방향 제어
    {
      digitalWrite(DIR, LOW);// CW 방향
    }
    else 
    {
      digitalWrite(DIR, HIGH); // CCW 방향
    }
    
    digitalWrite(SPEED,255);

    /* 실제 엔코더의 각도가 원하는 엔코더 각도 범주 안에 들어올 경우 */
    /* 브레이크를 작동하고 while문을 벗어난다 */
    if (encoderVal >= degree-1 && encoderVal <= degree+1)
    {
      digitalWrite(BRAKE,HIGH);
      break;
    }
  } // while문 괄호
} // loop문 괄호


/* encoderVal 변화량을 구하기 위한 함수*/
int getEncoderTurn(void)
{
  int result = 0;
  int newA = digitalRead(clpin);
  int newB = digitalRead(dtpin);
  
  if (newA != oldA || newB != oldB)
  {
    if (oldA == HIGH && newA == LOW)
    {
      result = (oldB * 2 - 1);
      if (minus_sig == 0)
      {
       result = (-1);  
      }
    }
  }
  
  oldA = newA;
  oldB = newB;
  return result;
}
