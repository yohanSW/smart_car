/* #define clpin 4 // 엔코더, 클락핀
#define dtpin 11 // 엔코더, 데이타핀
#define swpin 12 //엔코더, 스위치핀 */
#define brk_DIR 13 // 모터드라이버 -> 릴레이, LOW: CW / HIGH: CCW
#define brk_BRAKE 2 // 모터드라이버 -> 릴레이, LOW: brk_BRAKE 해제 / HIGH: brk_BRAKE
#define brk_SPEED 5 // 모터드라이버, PWM을 통한 모터 속도제어

int is_break = 0; // 차량 운행 정지 여부, 0: 운행 / 1: 정지
int is_breakING = 0; // 브레이크 모터가 동작 중인가? 0: 브레이크모터 동작 X / 1: 브레이크모터 동작 O

void setup() {
 pinMode (brk_BRAKE, OUTPUT);
 pinMode (brk_SPEED, OUTPUT);
 pinMode (brk_DIR, OUTPUT);
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
  }

  /* 정지와 관련된 동작 수행 부분 */
  if(is_break == 1 && is_breakING == 0) //정지 신호 발생, 그리고 원래 브레이크모터 동작은 없었음
  { 
    digitalWrite(brk_DIR,LOW); // 항상 CW방향으로 회전
    digitalWrite(brk_BRAKE,LOW); //정지 동작을 위해 브레이크 모터 고정 해제
    digitalWrite(brk_SPEED,255);
    delay(1500); // 1.5초 동안 브레이크 모터를 동작시켜 정지 동작 수행
    digitalWrite(brk_BRAKE,HIGH); // 차량 브레이크가 당겨진 상태로 고정
    is_breakING = 1; //브레이크모터가 동작중인데 loop를 돌아 중복하여 브레이크모터 동작 방지
  }
  else if(is_break ==1 && is_breakING == 1) // 여전히 정지 신호 발생, 브레이크 모터는 동작 중
  {
    delay(500);
  }
  else //정지 신호가 사라짐, 즉 주행모드로 전환
  {
    digitalWrite(brk_BRAKE,LOW); // 고정된 브레이크 모터 해제
    digitalWrite(brk_DIR,HIGH); // 당겨진 브레이크 모터 풀어주기 위해 방향 반대로 설정
    digitalWrite(brk_SPEED,255);
    delay(1500); // 1.5초 동안 브레이크 모터 해제
    digitalWrite(brk_BRAKE,HIGH); // 해체 한 상태로 브레이크 모터 고정
    is_breakING = 0; //브레이크모터는 더 이상 동작하지 않으므로, 다음 정지동작을 위해 0으로 초기화
  }
  
}

