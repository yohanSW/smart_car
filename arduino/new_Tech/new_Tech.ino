#include <CapacitiveSensor.h>

#define PROCESSING_VISUALIZER 1
#define SERIAL_PLOTTER  2

char RaspSignal = 'I'; //Raspberry Pi signal for various function in raspberryPi board ,I is Idle
int BrakeControl = 7;
int ClutchControl = 12;
int ClutchAlarm = 11;

//  Variables
int pulsePin = 0;                 // Pulse Sensor purple wire connected to analog pin 0
int blinkPin = 13;                // pin to blink led at each beat
int fadePin = 5;                  // pin to do fancy classy fading blink at each beat
int fadeRate = 0;                 // used to fade LED on with PWM on fadePin

//ultrasonic waves pin***************
int Trig_Pin = 9;
int Echo_Pin = 8;
//***********************************

//Vibration sensor*******************
#define vibration A1
//***********************************

//fire sensor*******************
int firePin = A2;
int fir = 0;

//Touch sensor*******************
int touch_result;
CapacitiveSensor   cs_4_2 = CapacitiveSensor(4,2);        // 10M resistor between pins 4 & 2, pin 2 is sensor pin, add a wire and or foil if desired

//***********************************
 
// Volatile Variables, used in the interrupt service routine!
volatile int BPM;                   // int that holds raw Analog in 0. updated every 2mS
volatile int Signal;                // holds the incoming raw data
volatile int IBI = 600;             // int that holds the time interval between beats! Must be seeded! 
volatile boolean Pulse = false;     // "True" when User's live heartbeat is detected. "False" when not a "live beat". 
volatile boolean QS = false;        // becomes true when Arduoino finds a beat.
 
// Regards Serial OutPut  -- Set This Up to your needs
static boolean serialVisual = true;   // Set to 'false' by Default.  Re-set to 'true' to see Arduino Serial Monitor ASCII Visual Pulse 
static int outputType = SERIAL_PLOTTER;
 
void setup(){
  pinMode(blinkPin,OUTPUT);         // pin that will blink to your heartbeat!
  pinMode(fadePin,OUTPUT);          // pin that will fade to your heartbeat!
  pinMode(vibration, INPUT);
  pinMode(firePin, INPUT);
  Serial.begin(115200);             // we agree to talk fast!
  interruptSetup();                 // sets up to read Pulse Sensor signal every 2mS 
   // IF YOU ARE POWERING The Pulse Sensor AT VOLTAGE LESS THAN THE BOARD VOLTAGE, 
   // UN-COMMENT THE NEXT LINE AND APPLY THAT VOLTAGE TO THE A-REF PIN
//   analogReference(EXTERNAL);   
  pinMode(Echo_Pin, INPUT);
  pinMode(Trig_Pin, OUTPUT);
  pinMode(BrakeControl,OUTPUT);
  pinMode(ClutchControl,OUTPUT);
  pinMode(ClutchAlarm,OUTPUT);
  
  cs_4_2.set_CS_AutocaL_Millis(0xFFFFFFFF);
}
 
 
//  Where the Magic Happens
void loop(){
  //Serial.print("@");
  //vivration pin*********************
  int vibration_num = 0;
  vibration_num = analogRead(vibration); 
  //Serial.print("vivration num : ");
  //Serial.println(vibration_num);

  //fire*****************************
  fir = analogRead(firePin);
  //Serial.print("fire num : ");
  //Serial.println(fir);  
    
  //ultrasonic waves pin***************
  long duration, distance;
  digitalWrite(Trig_Pin, HIGH);        
  delayMicroseconds(10);
  digitalWrite(Trig_Pin, LOW);
  duration = pulseIn(Echo_Pin, HIGH);
  distance = ((float)(340 * duration) / 10000) / 2;
  //Serial.print("거리:");         
  //Serial.print(distance);
  //Serial.println("cm");
  //***********************************

  //heart beat*************************
  //serialOutput() ;       
  if (QS == true){     // A Heartbeat Was Found
                       // BPM and IBI have been Determined
                       // Quantified Self "QS" true when arduino finds a heartbeat
        fadeRate = 255;         // Makes the LED Fade Effect Happen
                                // Set 'fadeRate' Variable to 255 to fade LED with pulse
        serialOutputWhenBeatHappens();   // A Beat Happened, Output that to serial.     
        QS = false;                      // reset the Quantified Self flag or next time    
  }
  ledFadeToBeat();                      // Makes the LED Fade Effect Happen 
  //***********************************

  //touch sensor***********************
  long start = millis();
  long touch =  cs_4_2.capacitiveSensor(500);
  if(touch>=300)
  {
    touch_result = 1;
  }
  else
  {
    touch_result = 0;
  }
  //Serial.print(millis() - start);        // check on performance in milliseconds
  //Serial.print("\t");                    // tab character for debug windown spacing
  //***********************************
  RaspSignal = Serial.read();
  if(RaspSignal == 'W') // to avoid the storage of sensor data in RaspberryPi board, during LED is blinked ,W is Wait
  {
    delay(14200); //LED blinked time
    RaspSignal = 'I';
  }
  else if(RaspSignal == 'B') // B is brake
  {
    digitalWrite(BrakeControl,HIGH);
    RaspSignal = 'I';
  }
  else if(RaspSignal == 'C') // C is Clutch control
  {
    digitalWrite(ClutchControl,LOW);
    RaspSignal = 'I';
  }
  else if(RaspSignal == 'A') // A is clutch Alarm
  {
    digitalWrite(ClutchAlarm,HIGH);
    RaspSignal = 'I';
  }
  else if(RaspSignal == 'N') // N is Normal
  {
    digitalWrite(BrakeControl,LOW);
    digitalWrite(ClutchControl,HIGH);
    digitalWrite(ClutchAlarm,LOW);
    RaspSignal = 'I';
  }
    Serial.println(vibration_num);
    Serial.println(fir);
    Serial.println(distance);
    Serial.println(BPM);
    Serial.println(touch_result);
    delay(900);
}
 
void ledFadeToBeat(){
    fadeRate -= 15;                         //  set LED fade value
    fadeRate = constrain(fadeRate,0,255);   //  keep LED fade value from going into negative numbers!
    analogWrite(fadePin,fadeRate);          //  fade LED
  }
