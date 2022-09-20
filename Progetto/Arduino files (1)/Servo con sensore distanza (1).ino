#include <Servo.h>

#define trigPin 13
#define echoPin 12
Servo myservo;

void setup() {

  Serial.begin (9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  myservo.attach(9);
  myservo.write(0);

}

void loop() {
 
  long duration, distance;
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2); 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10); 
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;
  if (distance < 4 || distance >50) {  // This is where the LED On/Off happens     digitalWrite(led,HIGH); // When the Red condition is met, the Green LED should turn off   digitalWrite(led2,LOW); }   else {     digitalWrite(led,LOW);     digitalWrite(led2,HIGH);   }   if (distance >= 200 || distance <= 0){
    Serial.println("Nessuna palla presente");
  }
  else {
    Serial.print(distance);
    Serial.println(" cm");
    myservo.write(90);
    delay(500);
    myservo.write(180);
    delay(300);
    
  }
  delay(500);
}