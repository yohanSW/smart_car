#include <Servo.h>
Servo myservo_x;
Servo myservo_y;

//#define photo_signal 4 // 사진찍는 신호
 
int pin_x = 0;
int pin_y = 1;
int pos_x = 0;
int pos_y = 0;


void setup() {
 myservo_x.attach(9);
 myservo_y.attach(10);
 //init
 myservo_x.write(90);
 myservo_y.write(90);
 Serial.begin(115200);
 pinMode(7,INPUT);

}

void loop() {
 int x = analogRead(pin_x);
 int y = analogRead(pin_y);
 int push = digitalRead(7);
 
 
 if(x<300){
  pos_x = constrain(--pos_x,0,180);
  myservo_x.write(pos_x);
 }
 else if(x>800){
  pos_x = constrain(++pos_x,0,180);
  myservo_x.write(pos_x);
 }
 
 if(y<300){
  pos_y = constrain(--pos_y,0,180);
  myservo_y.write(pos_y);
 }
 else if(y>800){
  pos_y = constrain(++pos_y,0,180);
  myservo_y.write(pos_y);
 }
 if (push == 1){
  Serial.println("1");
  //digitalWrite(photo_signal,HIGH);
  //digitalWrite(photo_signal,LOW);
 }
 else if (push ==0){
  Serial.println("0");
 }
 delay(15);
}
