#define clutch_pin 8 // automatic clutch pin
#define signalToMotor 9 // 자율주행 모드 변환 후 조향모터 작동을 위한 신호 발생
int signal_clutch = 0;

void setup() {
  pinMode(clutch_pin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  while(true){
    if(Serial.available()){
      signal_clutch = Serial.parseInt();
      Serial.print("FROM raspberry ");
      Serial.println(signal_clutch);
      if(signal_clutch ==1){
        Serial.println("Automatic clutch ON");
        digitalWrite(clutch_pin, HIGH);
        digitalWrite(signalToMotor, HIGH);
      }
      else{
        Serial.println("Automatic clutch OFF");
        digitalWrite(clutch_pin, LOW);
        digitalWrite(signalToMotor, LOW);
      }
    }
    else{
        digitalWrite(signalToMotor, LOW);
    }
  }
  

}
