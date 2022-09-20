//SPARAPALLONI TESINA IOT UNIMORE DI BRANDON WILLY VIGLIANISI

#include <Servo.h> 

//questi sono i due pin di trig ed echo del sensore di distanza
#define trigPin 13 
#define echoPin 12

//Definiamo qui i pin di ingresso
// Servono tre servo motori, un sensore di pressione(Bottone in prototipo), due sensori per
//   rilevare palla (prossimità o distanza) e dei led per gli idntificare gli stati

//Definisco dove collego i led
#define led_pin_Stato0  1
#define led_pin_Stato1  2
#define led_pin_Stato2  3
#define led_pin_Stato3  4
#define led_pin_Stato4  5
#define led_pin_Stato5  6

//Pin bottoni 
#define bottone1  7
#define bottone2  8

//servomotori

Servo dispenser; //fa entrare palloni in meccanismo lancio
Servo tenditore; //tende la molla per generare energia per il lancia
Servo grilletto; //rilascia meccanismo di lancio
Servo ricaricatore; //riporta braccio di lancio in posizione iniziale

// states: 0: 'Idle', 1: 'check disponibilità palla', 2: 'Faccio entrare palla', 3: 'Carica', 4: 'Sparo' , 5: 'Invia stat'
// Mentre lo stato è tra 1 e 4 voglio contare le statistiche
 
int iState; 
int iImposed;
int iFutureState;
int iReceived;
unsigned long time1; 
unsigned long time2; 
//unsigned long time3; 
long duration, distance;
int Stato_bottone1;
int Stato_bottone2;


void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  
  //inizializzo pin led come output
  pinMode(led_pin_Stato0, OUTPUT);
  pinMode(led_pin_Stato1, OUTPUT);
  pinMode(led_pin_Stato2, OUTPUT);
  pinMode(led_pin_Stato3, OUTPUT);
  pinMode(led_pin_Stato4, OUTPUT);
  pinMode(led_pin_Stato5, OUTPUT);
  
  //inizializzo pin bottoni come input
  pinMode(bottone1, INPUT);
  pinMode(bottone2, INPUT);
  
  //definisco pin del sensore di distanza
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  //inizializzo pin dei servo
  dispenser.attach(6);
  tenditore.attach(9);
  grilletto.attach(10);
  ricaricatore.attach(11);
  
  //inizializzo la posizione dei servo
  dispenser.write(90);
  tenditore.write(1);
  grilletto.write(90);
  ricaricatore.write(90);
  
  // initialize pin and value
  digitalWrite(led_pin_Stato0, LOW);
  digitalWrite(led_pin_Stato1, LOW);
  digitalWrite(led_pin_Stato2, LOW);
  digitalWrite(led_pin_Stato3, LOW);
  digitalWrite(led_pin_Stato4, LOW);
  digitalWrite(led_pin_Stato5, LOW);
  
  iState=0;
  iImposed=0;
  time1=millis();
  duration=2000;
  distance=60;
  iFutureState = 99;
  iReceived = -1;
  
  //inizializzo stati bottoni
  Stato_bottone1=0;
  Stato_bottone2=0;
}

void loop() {

  
  if (millis() - time1 > 10){ // read every 50 millisecond
	  
    time1 = millis();
        
    // Leggiamo valori sensore di prossimità
	digitalWrite(trigPin, LOW); 
	delayMicroseconds(2); 
	digitalWrite(trigPin, HIGH);
	delayMicroseconds(10); 
	digitalWrite(trigPin, LOW);
	duration = pulseIn(echoPin, HIGH);
	distance = (duration/2) / 29.1;
	
	//leggi valore sensore di pressione(bottone)
	Stato_bottone1 = digitalRead(bottone1);
	Stato_bottone2 = digitalRead(bottone2);

  } 
  

 

  if (Serial.available()>0) iReceived = Serial.read() - 48; //perchè se mando uno la seriale lo converte in ascii che è 49, 
															// 50 in ascii starebbe per 2 e così via fino al 9
    
    

    // default: back to the first state
   
	
	
	//Definizioni cambiamento di stato
    
    if (iState==0 && iReceived==1) iState=1;
    if (iState==1 && iReceived==0) iState=5;
    if (iState==2 && iReceived==0) iState=5;
    if (iState==3 && iReceived==0) iState=5;
    if (iState==4 && iReceived==0) iState=5;
    
    if (iState==1 && iImposed==2) iState=2;
    if (iState==2 && iImposed==3) iState=3;
    if (iState==3 && iImposed==4) iState=4;
    if (iState==4 && iImposed==1) iState=1;
    if (iState==5 && iImposed==0) iState=0;
 
    
    // CR and LF always skipped (no transition)
    if (iReceived==10 || iReceived==13){}1

  
	 Serial.println("iReceived=");
   Serial.println(iReceived);
   
	 if(iState==0){
		 digitalWrite(led_pin_Stato0, HIGH);
		 Serial.println("- Idle -");
	 } else if (iState==5 && iFutureState==0){
     digitalWrite(led_pin_Stato0, HIGH);
     Serial.println("- Ritornato ad Idle -");
	  } else {
		 digitalWrite(led_pin_Stato0, LOW);
	 }

     
     if (iState==1){
		 //controllo se ci sono palle disponibili
		 Serial.println("- Entrato in stato 1 -");
     Serial.println(distance);
		 if (distance >20) {  // This is where the LED On/Off happens     digitalWrite(led,HIGH); // When the Red condition is met, the Green LED should turn off   digitalWrite(led2,LOW); }   else {     digitalWrite(led,LOW);     digitalWrite(led2,HIGH);   }   if (distance >= 200 || distance <= 0){
			 Serial.println("- Nessuna palla presente -"); //al posto della scritta magari è meglio un
			 // codice che poi il bridge interpreta e manda un segnale ad un feed che avvisa l'app di ciò
			 //magari qui accendiamo un led per segnalare che non ci sono palloni 
         } else {
				 //Serial.print(distance);//Serial.println(" cm");
				 digitalWrite(led_pin_Stato1, HIGH);
				 Serial.println("- Palla disponibile -");
         time2 = millis();
				 iImposed=2;
				 }
	 }
	 
     if (iState==2){
		 Serial.println("- Entrato in stato 2 -");
		 //Fai entrare palla in meccanismo
		 
		 if ((millis() - time2) > 1000){ //vedi un un po' poi dalla pratica che valore mettere dopo il >
			 dispenser.write(90);
			 Serial.println("- Palla fatta entrare passo al 3 -");
			 iImposed=3;
		 } else {
		  dispenser.write(180);
		  }
	 }
	 
     if (iState==3){
		 //carica
		 Serial.println("- Carico meccanismo -");
     delay(500);
		 iImposed=4;
	 }
	 
     if (iState==4){
		 //Spara e torna allo stato 1 per ripetere il ciclo
		 Serial.println("- Sparo e torno a passo 1 -");
    delay(500);
		 iImposed=1;
	 }
	 
	 if (iState==5){
		 //Quando chiudo la sessione di tiro devo salvare ed inviare le statistiche
		 
		 //Così di costruisce un pacchetto da inviare nella seriale con i valori dei 
		 //  sensori mappandoli dall'originale 0->1024 a 0->253. 
		 //Potrei usare un pacchetto di quattro dati con tirati e realizzati da due e tre punti
		 /*Serial.write(0xff); //flag di inizio pacchetto
		 Serial.write(0x02); //qua dico quanti dati invio in questo caso 2 (0x01 starebbe per 1)
		 Serial.write((char)(map(sensorValue1,0,1024,0,253))); //dato1 (potrei mettere qui tirati o posizione)
		 Serial.write((char)(map(sensorValue2,0,1024,0,253))); //dato2 (potrei mettere i realizzati)
		 Serial.write(0xfe);*/  //flag di fine pacchetto
		 Serial.println("- Invio statistiche e torno in idle -");
		 iImposed=0;//alla fine ritorno allo stato di idle
	 }
     
     
 

     //Conteggio Statistiche
	 if (iState>0 && iState<5){
		 //computa statistiche
     delay(500);
		 Serial.println("- Sto tenendo le statistiche -");
		 
	 }

       // state transition (Noi queste transizioni di stato le faremo dentro gli stati stessi 
   
	 
	 delay(1);
}
