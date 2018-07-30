#define clutch_pin 8 // automatic clutch pin
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
      }
      else{
        Serial.println("Automatic clutch OFF");
        digitalWrite(clutch_pin, LOW);
      }
    }
    else{
      //Serial.println("111Automatic clutch OFF");
       //digitalWrite(clutch_pin, LOW);
    }
  }
  

}
