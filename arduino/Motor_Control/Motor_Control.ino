/* 3조 모터컨트롤 코드*/
/* 엔코더 부분 */
#define clpin 4 // 엔코더, 클락핀
#define dtpin 11 // 엔코더, 데이타핀
#define swpin 12 //엔코더, 스위치핀

/* 조향 모터 부분 */
#define mt_STOP 8 // 모터드라이버 -> 릴레이, LOW: 모터 작동 / HIGH: 모터 정지 
#define mt_DIR 7 // 모터드라이버 -> 릴레이, LOW: CW / HIGH: CCW
#define mt_SPEED 5 // 모터드라이버, PWM을 통한 모터 속도제어
#define gear_ratio 0.162 // 스티어링과 엔코더의 기어비 (73/25)*(20/360) {3조}
//#define gear_ratio 0.18 // 스티어링과 엔코더의 기어비 (108/25)*(15/360) {2조}

/* 브레이크 모터 부분 */
#define brk_DIR 13 // 모터드라이버 -> 릴레이, LOW: CW / HIGH: CCW
#define brk_RELEASE 2 // 모터드라이버 -> 릴레이, HIGH: 브레이크 모터 정지 / LOW: 브레이크 모터 작동
#define brk_SPEED 5 // 모터드라이버, PWM을 통한 모터 속도제어

/* 자율주행여부, 브레이크제어 코드 */
#define auto_DRI 9 // 자율주행 여부를 아두이노 신호로 받음  (1 : 자율주행 0 : 수동주행)
#define auto_STOP 10  //2조 
int is_driving = 0;
int brake_order = 0;
int encoder_boundary = 84; // {3조}
//int encoder_boundary = 102; // {2조}

double steer_angle; // 회전시키고자 하는 스티어링 각도
double degree; // 회전시키고자 하는 엔코더 각도
/*모터 -> 스티어링 -> 엔코더*/

/* Encoder Value 초기화 */
int encoderVal = 0; 
int mt_ctrl_cnt = 0;
static int oldA = HIGH;
static int oldB = HIGH;

/* Serial 통신 초기화 */
long wheel_angle=0; // 조향각 (바퀴의 각도)
int minus_sig=1; // 조향각 (바퀴의 각도)
int is_brake=0; // 차량 운행 정지 여부, 0: 운행 / 1: 정지
int is_brakeING = 0; // 브레이크 모터가 동작 중인가? 0: 브레이크모터 동작 X / 1: 브레이크모터 동작 O

void setup() {
 pinMode (clpin, INPUT);
 pinMode (dtpin, INPUT);
 pinMode (swpin, INPUT);
 pinMode (mt_STOP, OUTPUT);
 pinMode (mt_SPEED, OUTPUT);
 pinMode (mt_DIR, OUTPUT);
 pinMode (brk_RELEASE, OUTPUT);
 pinMode (brk_SPEED, OUTPUT);
 pinMode (brk_DIR, OUTPUT);
 pinMode (auto_DRI, INPUT);
 pinMode (auto_STOP, INPUT); 
 digitalWrite (brk_RELEASE , LOW); // 데이터를 입력받기 전엔 브레이크 모터는 정지상태로 시작
 digitalWrite (swpin, HIGH); // encoder 동작을 위한 switch ON
 digitalWrite (mt_STOP, HIGH); // 데이터를 입력받기 전엔 모터는 정지상태로 시작
 Serial.begin(9600);
}



void loop() {
  /* 입력가능한 불가능한 상태일 경우, while문 무한루프. 즉, 대기상태 */
  get_data();

  steer_angle = wheel_angle * 13 ; // 스티어링 각도와 조향 각도의 비 13 : 1
  degree = steer_angle * gear_ratio;

  //자율주행 모드 
  if(is_driving != 0){
    brake_mode(); // 브레이크 작동여부 체크
    control(degree); // 조향 작동
  }
  //수동주행 모드
  else{
    encoderVal = encoderVal + getEncoderTurn(); // encoder 각도 갱신, encoder 값이 틀어지는 것을 방지하는것
    digitalWrite(mt_STOP,HIGH); // 조향모터 정지 
  }
    
} // loop문 괄호


void get_data(){
    /* 입력가능한 불가능한 상태일 경우, while문 무한루프. 즉, 대기상태 */
  while(true) 
  {
    
    is_driving = digitalRead(auto_DRI);  // 선택사항 -> 자율주행 모드 연결시 사용(아두이노에서 넘어오는 신호, 모터 작동 여부 결정)
    //is_driving = 1;      
    /*2조        
    brake_order = digitalRead(auto_STOP);
    */
    
    if(Serial.available())
    {
      if(Serial.find('#'))
      {
        minus_sig = Serial.parseInt();
        wheel_angle=Serial.parseInt();
        if(minus_sig == 0)
          wheel_angle = -wheel_angle;
        /* 2조
        is_brake = Serial.parseInt();
        if(is_brake == 1 || brake_order ==1)
          is_brake = 1;
        */
        Serial.print("wheel_angle : ");
        Serial.println(wheel_angle); //0.5초 딜레이 동안 받는 신호 수 만큼 angle 출력
        
      }
      else
        continue;
      break;
    }
    else
      continue;
  }
}

void brake_mode(){
  // 브레이크 잠긴 상태로 신호가 꺼졌을 경우 대비용
    if (is_break == 2)
  {
    digitalWrite(brk_DIR,HIGH); // 당겨진 브레이크 모터 풀어주기 위해 방향 반대로 설정
    digitalWrite(brk_RELEASE,LOW); // 고정된 브레이크 모터 해제
    digitalWrite(brk_SPEED,255);
    delay(700); 브레이크 모터 해제
    digitalWrite(brk_RELEASE,HIGH); // 해체 한 상태로 브레이크 모터 고정
    is_brakeING = 0; //브레이크모터는 더 이상 동작하지 않으므로, 다음 정지동작을 위해 0으로 초기화
  }
  if(is_brake == 1 && is_brakeING == 0) //정지 신호 발생, 그리고 원래 브레이크모터 동작은 없었음
  { 
    digitalWrite(brk_DIR,LOW); // 항상 CW방향으로 회전
    digitalWrite(brk_RELEASE,LOW); //정지 동작을 위해 브레이크 모터 고정 해제   
    digitalWrite(brk_SPEED,255);   
    delay(700); // 1.5초 동안 브레이크 모터를 동작시켜 정지 동작 수행   
    digitalWrite(brk_RELEASE,HIGH); // 차량 브레이크가 당겨진 상태로 고정
    is_brakeING = 1; //브레이크모터가 동작중인데 loop를 돌아 중복하여 브레이크모터 동작 방지
  }
  else if(is_brake ==1 && is_brakeING == 1) // 여전히 정지 신호 발생, 브레이크 모터는 동작 중
  {
    delay(500);
  }
  else if(is_brake == 0 && is_brakeING == 1) // 브레이크 밟힌 상태, 정지 신호 해제
  {
    digitalWrite(brk_DIR,HIGH); // 당겨진 브레이크 모터 풀어주기 위해 방향 반대로 설정
    digitalWrite(brk_RELEASE,LOW); // 고정된 브레이크 모터 해제
    digitalWrite(brk_SPEED,255);
    delay(700); 브레이크 모터 해제
    digitalWrite(brk_RELEASE,HIGH); // 해체 한 상태로 브레이크 모터 고정
    is_brakeING = 0; //브레이크모터는 더 이상 동작하지 않으므로, 다음 정지동작을 위해 0으로 초기화
  }
  else ;// 정시 신호 없음, 그리고 브레이크 동작도 없었음. 즉 정상주행
}

/* encoderVal 변화량을 구하기 위한 함수*/
int getEncoderTurn(void)
{
  int result = 0;
  int newA = digitalRead(clpin);
  int newB = digitalRead(dtpin);
  if (newA != oldA || newB != oldB)
    if (oldA == HIGH && newA == LOW)
    {
      result = (oldB * 2 - 1);
      /*
      if (minus_sig == 0)
       result = (-1);  
       */
    }

  oldA = newA;
  oldB = newB;
  return result;
}

void control(int degree){
  /* 엔코더 조향각이 바뀔 때마다 steer_angle입력을 막기 위해 while문 추가*/
  while(1)
  {
    
   int change = getEncoderTurn(); // encoder 각도 변화량
    encoderVal = encoderVal + change; // encoder 각도 갱신
    /* encoder 각도계산 종료시 초기화, 자율주행 종료시 switch OFF */
    if (digitalRead(swpin) == LOW)
      encoderVal = 0;

    Serial.print("encoderVal : ");  
    Serial.println(encoderVal);
    digitalWrite(mt_STOP,LOW); // 모터동작을 시작하기 위해 브레이크 해제
    if (encoderVal <= degree) // 방향 제어
      digitalWrite(DIR, LOW);// CW 방향
    else 
      digitalWrite(DIR, HIGH); // CCW 방향
    digitalWrite(SPEED,255);

    /* 실제 엔코더의 각도가 원하는 엔코더 각도 범주 안에 들어올 경우 */
    /* 브레이크를 작동하고 while문을 벗어난다 */
    if ( encoderVal >= degree-2 && encoderVal <= degree+2 ){
      digitalWrite(mt_STOP,HIGH);
      mt_ctrl_cnt=0;
      brake;
    }
   else if(encoderVal >= encoder_boundary || encoderVal <= -encoder_boundary ){
      digitalWrite(mt_STOP,HIGH);
      if(encoderVal >= encoder_boundary){
        encoderVal = encoderVal - 1;
        mt_ctrl_cnt++;
      }
      else {
        encoderVal = encoderVal + 1;
        mt_ctrl_cnt--;
      }
      brake;
    }
    
    if(mt_ctrl_cnt == 1){
      if(encoderVal == encoder_boundary-mt_ctrl_cnt){;}
      else{
      //Serial.println(mt_ctrl_cnt);
      encoderVal = encoderVal + mt_ctrl_cnt;
      mt_ctrl_cnt=0;
      }
     }
     else if(mt_ctrl_cnt== -1){
      if(encoderVal == -encoder_boundary - mt_ctrl_cnt){;}
      else{
      //Serial.println(mt_ctrl_cnt);
      encoderVal = encoderVal + mt_ctrl_cnt;
      mt_ctrl_cnt=0;
      }
     }
  } // while문 괄호
}
