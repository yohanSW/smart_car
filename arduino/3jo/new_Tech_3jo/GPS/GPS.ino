#include <SoftwareSerial.h>
SoftwareSerial gpsSerial(11,12);
String buf;
char charbuf[76];
String latitude;
String latitude2;
double latitude3;
String longitude;
String longitude2;
double longitude3;
String sdate;
String stime;
int i;
int val;

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);
  delay(1000);
}

void loop() {
  if (gpsSerial.available()){
    char val2 = gpsSerial.read() ;
    buf += val2;
    if (val2 == '\n'){
      if (buf.startsWith("$GPRMC",0)) buf.toCharArray(charbuf,76);
      for (i=19 ; i<21; i++) latitude += charbuf[i]; 
      for (i=21 ; i<29; i++) latitude2 += charbuf[i];
      latitude3 = (latitude2.toDouble())/60.0 + latitude.toDouble();
      //latitude3=(latitude2.toDouble())/60.0;
      for (i=32 ; i<35; i++) longitude += charbuf[i];
      for (i=35 ; i<43; i++) longitude2 += charbuf[i];
      longitude3 = ((longitude2.toDouble())/60.0) + longitude.toDouble();
      for (i=53 ; i<59; i++) sdate += charbuf[i]; //DDMMYY
      for (i=7 ; i<13; i++) stime += charbuf[i]; // HHMMSS Greenwich mean time
      
      Serial.print("Total Latitude: ");
      Serial.print(latitude3); 
      //Serial.println((latitude2.toDouble()));
      //Serial.println(charbuf[30]);
      Serial.print("Total Longitude: ");
      Serial.println(longitude3);
      //Serial.println(charbuf[44]);
      //Serial.print("Latitude to Double : ");
      //Serial.println(latitude2);
      //Serial.print("Latitude to Double /60 : ");
      //double a=((latitude2.toDouble()*100000)/60.0);
      //Serial.println(a);
      //Serial.println((latitude2.toDouble()*100000)/60.0);
      //Serial.println(a/100000+a%100000.0);
      //Serial.println(latitude.toDouble()+latitud
      
      buf="";
      latitude="";
      latitude2="";
      longitude="";
      longitude2="";
      stime="";
      sdate="";
      delay(1000);
    }
  }
}
