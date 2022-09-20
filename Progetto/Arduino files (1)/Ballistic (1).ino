#include <Servo.h>


Servo dispenser;
Servo tenditoreuno;
Servo tenditoredue;
Servo grilletto;
Servo ricaricatore;


void setup(){
  
  dispenser.attach(8);
  tenditoreuno.attach(7);
  tenditoredue.attach(9);
  grilletto.attach(10);
  ricaricatore.attach(11);
  
  dispenser.write(90);
  tenditoreuno.write(1);
  tenditoredue.write(1);
  grilletto.write(90);
  ricaricatore.write(90);
  }

void loop(){
  	grilletto.write(90);
  	delay(500);
  	dispenser.write(90);
  	delay(500);
  	dispenser.write(1);
    delay(1000);
    dispenser.write(90);
  	delay(1000);
    tenditoreuno.write(120);
  	tenditoredue.write(120);
    delay(1000);
    grilletto.write(1);
    delay(500);
  	tenditoreuno.write(1);
  	tenditoredue.write(1);
  	delay(500);
    ricaricatore.write(1);
    delay(1000);
    ricaricatore.write(90);
  	delay(1000);
}