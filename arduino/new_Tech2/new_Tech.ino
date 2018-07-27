#define PROCESSING_VISUALIZER 1
#define SERIAL_PLOTTER  2

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
}
 
 
//  Where the Magic Happens
void loop(){
  //Serial.print("@");
  //vivration pin*********************
  int vibration_num = 0;
  vibration_num = analogRead(vibration); 
  //Serial.print("vivration num : ");
  //Serial.println(vibration_num);
   if(vibration_num > 10)
      vibration_num = 1;
    else
      vibration_num = 0;

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
        QS = false;                      // reset the Quantified Self flag for next time    
  }
  ledFadeToBeat();                      // Makes the LED Fade Effect Happen 
  //***********************************
  Serial.println(vibration_num);
  Serial.println(fir);
  Serial.println(distance);
  Serial.println(BPM);
  delay(500);                             //  take a break
}
 
void ledFadeToBeat(){
    fadeRate -= 15;                         //  set LED fade value
    fadeRate = constrain(fadeRate,0,255);   //  keep LED fade value from going into negative numbers!
    analogWrite(fadePin,fadeRate);          //  fade LED
  }
