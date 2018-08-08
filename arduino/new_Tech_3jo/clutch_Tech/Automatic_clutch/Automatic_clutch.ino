#define clutch_pin 8 // automatic clutch pin -> 클러치 결착 신호
#define signalToMotor 9 // 자율주행 모드 변환 후 조향모터 작동을 위한 신호 발생 -> 자율주행 할지 말지 
int signal_clutch = 0;

void setup() {
  pinMode(clutch_pin, OUTPUT); // 전자클러치로 연결되는 아웃풋
  pinMode(signalToMotor, OUTPUT); // 라즈베리파이로 연결되는 아웃풋
  Serial.begin(9600);
}

void loop() {
  while(true){
    if(Serial.available()){
      signal_clutch = Serial.parseInt(); // 보이스키트에서 자유주행관련 신호 전달 받음
      Serial.print("FROM raspberry ");
      Serial.println(signal_clutch);
      if(signal_clutch ==1){
        Serial.println("Automatic clutch ON");
        digitalWrite(clutch_pin, HIGH); // 전자클러치 연결
        digitalWrite(signalToMotor, HIGH); // 메인 라즈베리에 신호 보냄
      }
      else{
        Serial.println("Automatic clutch OFF");
        digitalWrite(clutch_pin, LOW); // 전자클러치 해제
        digitalWrite(signalToMotor, LOW);
      }
    }
    else{
        #digitalWrite(signalToMotor, LOW); // 아두이노는 기본으로 1값을 가지기 때문에 필요 없음 
    }
  }
  

}
