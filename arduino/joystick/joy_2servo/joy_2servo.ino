#include <Servo.h>

//CONSTANTS
const int servoUD = 4;       // servo for Up and Down motion
const int servoLR = 10;       // servo for Left and Right motion

//VARIABLE
int VRx = 3;        // VRx Thumbstick
int VRy = 4;        // VRy Thumbstick
int SW = 0;       // SW Thumbstick
int VRxPos = 90;
int VRyPos = 90;
int SWPos = 90;
boolean logging = false;

int vrx_pre;
int vry_pre;
Servo myservoUD;  // create servo object to control a servo for UD motion
Servo myservoLR;  // create servo object to control a servo for LR motion

void setup() {

 // Servo  
 myservoUD.attach(servoUD);  // attaches the servo
 myservoLR.attach(servoLR);  // attaches the servo
             

 // Inizialize Serial
 Serial.begin(9600);
}


void loop(){

   // Display Joystick values using the serial monitor
   outputJoystick();

   // Read the horizontal joystick value  (value between 0 and 1023)
   VRxPos = analogRead(VRx);          
   VRxPos = map(VRxPos, 0, 1023, 0, 180);     // scale it to use it with the servo (result  between 0 and 180)

   myservoLR.write(VRxPos);                         // sets the servo position according to the scaled value    

   // Read the horizontal joystick value  (value between 0 and 1023)
   VRyPos = analogRead(VRy);           
   VRyPos = map(VRyPos, 0, 1023, 0, 180);     // scale it to use it with the servo (result between 70 and 180)

   myservoUD.write(VRyPos);                           // sets the servo position according to the scaled value

   vrx_pre = VRx;
   vry_pre = VRy;

   delay(50);                                       // waits for the servo to get there

}


/**
* Display joystick values
*/
void outputJoystick(){

   Serial.print(VRxPos);
   Serial.print ("---"); 
   Serial.print(VRyPos);
   Serial.println ("----------------");
   Serial.print(SWPos);     
   Serial.println("------------");

}
