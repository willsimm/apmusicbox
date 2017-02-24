#include "Keyboard.h"

//FLEX SENSOR
//https://learn.sparkfun.com/tutorials/flex-sensor-hookup-guide
const int FLEX_PIN = A0; // Pin connected to voltage divider output

//END FLX SENSOR

//FSR
//http://bildr.org/2012/11/force-sensitive-resistor-arduino/
int FSR_Pin = A1; //analog pin 1
char lastFSRKey = 'c';
//END FSR



float maxFSRReading = 800;
float minFSRReading = 0;
float maxFlexReading = 600;
float minFlexReading = 300;


void setup()
{
  Serial.begin(9600);

  //FLEX
  pinMode(FLEX_PIN, INPUT);

  //FSR
  pinMode(FSR_Pin, INPUT);

  

}









//read the flex sensor and then map to a key, write it if theres a change
int readFlexSensor(){

  // Read the ADC, and calculate voltage and resistance from it
  int flexADC = analogRead(FLEX_PIN);
  
   if (flexADC > maxFlexReading){
    maxFlexReading = flexADC;
  }
  if (flexADC < minFlexReading){
    minFlexReading = flexADC;
  }

  //Serial.println(flexADC);

 float reading = ( (flexADC - minFlexReading) / (maxFlexReading - minFlexReading) ) *100;
 reading = 100 - reading;

  return (int)reading;

}

int readFSR(){

  int FSRReading = analogRead(FSR_Pin);

//Serial.println(FSRReading);
  if (FSRReading > maxFSRReading){
    maxFSRReading = FSRReading;
  }
  if (FSRReading < minFSRReading){
    minFSRReading = FSRReading;
  }

  

 float reading = ( (FSRReading - minFSRReading) / (maxFSRReading - minFSRReading) ) *100;


  return (int)reading;
}



void loop()
{
  int flex = readFlexSensor();
  int force = readFSR();
  String op = (String)flex + "#" + force;
   Serial.println(op);
  // Serial.println(reading);


  
  delay(50);

}


