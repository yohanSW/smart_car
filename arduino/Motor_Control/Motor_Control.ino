#define clpin 2
#define dtpin 3
#define swpin 4

int encoderVal = 0;
double degree = 37;
static int oldA = HIGH;
static int oldB = HIGH;

void setup() {
  pinMode (clpin, INPUT);
  pinMode (dtpin, INPUT);
  pinMode (swpin, INPUT);
  pinMode (8, OUTPUT);
  pinMode (5, OUTPUT);
  digitalWrite (swpin, HIGH);
  Serial.begin(9600);
}

void loop() {
  int change = getEncoderTurn();
  encoderVal = encoderVal + change;
  if (digitalRead(swpin) == LOW)
  {
    encoderVal = 0;
  }
  Serial.println(encoderVal);
  digitalWrite(8,LOW); // 브레이크 해제
 /*if (encoderVal <= degree)
 {
  digitalWrite(7, HIGH);//방향 바꿈
 }
 else 
 {
  digitalWrite(7, LOW); // 방향 바꿈
 }*/
 digitalWrite(5,255);
 if (encoderVal >= degree-2 && encoderVal <= degree+2)
 {
  digitalWrite(8,HIGH);
 }
 
}


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
    }
  }
  oldA = newA;
  oldB = newB;
  return result;
}
