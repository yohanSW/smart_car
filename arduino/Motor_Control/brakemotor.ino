/* #define clpin 4 // 엔코더, 클락핀
#define dtpin 11 // 엔코더, 데이타핀
#define swpin 12 //엔코더, 스위치핀 */
#define brk_DIR 13 // 모터드라이버 -> 릴레이, LOW: CW / HIGH: CCW
#define brk_BRAKE 2 // 모터드라이버 -> 릴레이, HIGH: brk_BRAKE 해제 / LOW: brk_BRAKE
#define brk_SPEED 5 // 모터드라이버, PWM을 통한 모터 속도제어


double steer_angle; // 회전시키고자 하는 스티어링 각도
double degree; // 회전시키고자 하는 엔코더 각도

/* Encoder Value 초기화 */
int encoderVal = 0; 
static int oldA = HIGH;
static int oldB = HIGH;

/* Serial 통신 초기화 */
long wheel_angle=0; // 조향각 (바퀴의 각도)
int minus_sig=1; // 조향각 (바퀴의 각도)


int is_break = 0; // 차량 운행 정지 여부, 0: 운행 / 1: 정지
int is_breakING = 0; // 브레이크 모터가 동작 중인가? 0: 브레이크모터 동작 X / 1: 브레이크모터 동작 O

void setup() {
 pinMode (brk_BRAKE, OUTPUT);
 pinMode (brk_SPEED, OUTPUT);
 pinMode (brk_DIR, OUTPUT);
 Serial.begin(9600);
}

void loop() {
  
  while(true) 

  {

    Serial.flush();

    delay(500);

    if(Serial.available())

    {

      while(Serial.find('#'))

      {

        minus_sig = Serial.parseInt();

        wheel_angle=Serial.parseInt();

        if(minus_sig == 0)

          wheel_angle = -wheel_angle;

        is_break = Serial.parseInt();

        Serial.print(wheel_angle); //0.5초 딜레이 동안 받는 신호 수 만큼 angle 출력

      }

      break;

    }

    else

      continue;

  }

  /* 정지와 관련된 동작 수행 부분 */
  if(is_break == 1 && is_breakING == 0) //정지 신호 발생, 그리고 원래 브레이크모터 동작은 없었음
  { 
    Serial.println("11");
    digitalWrite(brk_DIR,LOW); // 항상 CW방향으로 회전
    digitalWrite(brk_BRAKE,HIGH); //정지 동작을 위해 브레이크 모터 고정 해제
    delay(300);
    digitalWrite(brk_SPEED,255);
    Serial.println("ddd");
    delay(5000); // 1.5초 동안 브레이크 모터를 동작시켜 정지 동작 수행
    digitalWrite(brk_BRAKE,LOW); // 차량 브레이크가 당겨진 상태로 고정
    is_breakING = 1; //브레이크모터가 동작중인데 loop를 돌아 중복하여 브레이크모터 동작 방지
  }
  else if(is_break ==1 && is_breakING == 1) // 여전히 정지 신호 발생, 브레이크 모터는 동작 중
  {
    Serial.println("222");
    delay(500);
  }
  else if(is_break == 0 && is_breakING == 1) // 브레이크 모터 동작중, 정지 신호 해제
  {
    digitalWrite(brk_DIR,HIGH); // 당겨진 브레이크 모터 풀어주기 위해 방향 반대로 설정
    digitalWrite(brk_BRAKE,HIGH); // 고정된 브레이크 모터 해제
    delay(300);
    digitalWrite(brk_SPEED,255);
    Serial.println("333");
    delay(5000); // 1.5초 동안 브레이크 모터 해제
    digitalWrite(brk_BRAKE,LOW); // 해체 한 상태로 브레이크 모터 고정
    is_breakING = 0; //브레이크모터는 더 이상 동작하지 않으므로, 다음 정지동작을 위해 0으로 초기화
  }
  else // 정시 신호 없음, 그리고 브레이크 동작도 없었음. 즉 정상주행
  {
     Serial.println("555");
  }
  
}
