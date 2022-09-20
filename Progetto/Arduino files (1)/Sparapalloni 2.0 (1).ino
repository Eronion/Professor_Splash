//SPARAPALLONI TESINA IOT UNIMORE DI BRANDON WILLY VIGLIANISI

#include <Servo.h> 

//questi sono i quattro pin di trig ed echo dei due sensori di distanza(check palla e canestri realizzati)
#define trigPin1 13 
#define echoPin1 12
#define trigPin2 15 
#define echoPin2 14

//Definiamo qui i pin di ingresso
// Servono tre servo motori, un sensore di pressione(Bottone in prototipo), due sensori per
//  rilevare palla (prossimità o distanza) e dei led per gli idntificare gli stati

//Definisco dove collego i led
#define led_pin_StatoIdle  1
#define led_pin_StatoOn  2
#define led_pin_Stato2  3
#define led_pin_Stato3  4
#define led_pin_Stato4  5
#define led_pin_Stato5  6

//Pin bottoni 
#define bottone_2punti  7 
#define bottone_3punti  8

//servomotori
Servo dispenser; //fa entrare palloni in meccanismo lancio
Servo tenditore; //tende la molla per generare energia per il lancia
Servo grilletto; //rilascia meccanismo di lancio
Servo ricaricatore; //riporta braccio di lancio in posizione iniziale

// STATES: 0: 'Idle', 1: 'check disponibilità palla', 2: 'Faccio entrare palla', 3: 'Carica', 4: 'Sparo' , 5: 'Invia stat'
// Mentre lo stato è tra 1 e 4 voglio contare le statistiche
 
int iState; 
int iImposed;
int iFutureState;
int iReceived;
unsigned long time1; 
unsigned long time2; 
long duratioce_check, distance_check;
long duration_realizzati, distance_realizzati;
int Stato_bottone_2punti;
int Stato_bottone_3punti;
int tirati_2punti;
int tirati_2punti;
int realizzati_3punti;
int realizzati_3punti;


void setup() {
	
	// initialize serial communications at 9600 bps:
	Serial.begin(9600);
  
	//inizializzo pin led come output
	pinMode(led_pin_StatoIdle, OUTPUT);
	pinMode(led_pin_StatoOn, OUTPUT);
	pinMode(led_pin_Stato2, OUTPUT);
	pinMode(led_pin_Stato3, OUTPUT);
	pinMode(led_pin_Stato4, OUTPUT);
	pinMode(led_pin_Stato5, OUTPUT);
  
	//inizializzo pin bottoni come input
	pinMode(bottone_2punti, INPUT);
	pinMode(bottone_3punti, INPUT);
  
	//definisco pin del sensore di distanza
	pinMode(trigPin1, OUTPUT);
	pinMode(echoPin1, INPUT);
	pinMode(trigPin2, OUTPUT);
	pinMode(echoPin2, INPUT);
  
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
	digitalWrite(led_pin_StatoIdle, LOW);
	digitalWrite(led_pin_StatoOn, LOW);
	digitalWrite(led_pin_Stato2, LOW);
	digitalWrite(led_pin_Stato3, LOW);
	digitalWrite(led_pin_Stato4, LOW);
	digitalWrite(led_pin_Stato5, LOW);
  
	iState=0;
	iImposed=0;
	time1=millis();
	duration_check=2000;
	distance_realizzati=60;
	duration_realizzati=2000;
	distance_check=60;
	//iFutureState = 99;
	iReceived = -1;
  
	//inizializzo stati bottoni
	Stato_bottone_2punti=0;
	Stato_bottone_3punti=0;
  
	//inizializzo stats
	tirati_2punti=0;
	tirati_3punti=0;
	realizzati_2punti=0;
	realizzati_3punti=0;
}

void loop() {

	if (millis() - time1 > 10){ // read every 50 millisecond
	time1 = millis();
   
    // Leggiamo valori sensore di prossimità
	digitalWrite(trigPin1, LOW); 
	delayMicroseconds(2); 
	digitalWrite(trigPin1, HIGH);
	delayMicroseconds(10); 
	digitalWrite(trigPin1, LOW);
	duration_check = pulseIn(echoPin1, HIGH);
	distance_check = (duration_check/2) / 29.1;
	
	digitalWrite(trigPin2, LOW); 
	delayMicroseconds(2); 
	digitalWrite(trigPin2, HIGH);
	delayMicroseconds(10); 
	digitalWrite(trigPin2, LOW);
	duration_realizzati = pulseIn(echoPin2, HIGH);
	distance_realizzati = (duration_realizzati/2) / 29.1;
	
	//leggi valore sensore di pressione(bottone)
	Stato_bottone_2punti = digitalRead(bottone_2punti);
	Stato_bottone_3punti = digitalRead(bottone_3punti);

  } 
  

 

	if (Serial.available()>0) iReceived = Serial.read() - 48; //perchè se mando uno la seriale lo converte in ascii che è 49, 
															// 50 in ascii starebbe per 2 e così via fino al 9
    
    

    // default: back to the first state
   
	
	
	//Definizioni cambiamento di stato
    
    if (iState==0 && iReceived==1) iState=1; //On
	
    if (iState==1 && iReceived==0) iState=0; //Off
    //Permetto di spegnere la macchina solo nello stato 1 per evitare di lasciare la macchina in uno stato inconsistente
    
	if (iReceived==2) iState=5 //cancello statistiche 
	
	if (iReceived==9) iState=0; //Emergency stop
    
    if (iState==1 && iImposed==2) iState=2; //Ciclo degli stati
    if (iState==2 && iImposed==3) iState=3;
    if (iState==3 && iImposed==4) iState=4;
    if (iState==4 && iImposed==1) iState=1;
    if (iState==5 && iImposed==0) iState=0;
	
	//Potrei imporre un nuovo stato che azzera le statistiche ma fa continuare il ciclo della sparapalloni
 
    
    // CR and LF always skipped (no transition) 
	//anche se non mi serve a molto visto che lavoro con numeri e non con caratteri
    //if (iReceived==10 || iReceived==13){} //salta a capo
    if (iReceived>9 || iReceived<0){}
   
	if(iState==0){ //magari fai due led separati uno rosso che dice quando è in idle e uno verde per quando è in funzione
		digitalWrite(led_pin_StatoIdle, HIGH);
		digitalWrite(led_pin_StatoOn, LOW);
		Serial.println("- Idle -");
	 } else {
		digitalWrite(led_pin_StatoIdle, LOW);
		digitalWrite(led_pin_StatoOn, HIGH);
	}

    if (iState==1){
		 //controllo se ci sono palle disponibili
		 Serial.println("- Entrato in stato 1 -");
		if (distance >20) {  // This is where the LED On/Off happens     digitalWrite(led,HIGH); // When the Red condition is met, the Green LED should turn off   digitalWrite(led2,LOW); }   else {     digitalWrite(led,LOW);     digitalWrite(led2,HIGH);   }   if (distance >= 200 || distance <= 0){
			 Serial.println("- Nessuna palla presente -"); //al posto della scritta magari è meglio un
			 // codice che poi il bridge interpreta e manda un segnale ad un feed che avvisa l'app di ciò
			 //magari qui accendiamo un led per segnalare che non ci sono palloni 
        } else {
				//Serial.print(distance);//Serial.println(" cm");
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
		 //conto tirati
		 if(Stato_bottone_2punti==1) tirati_2punti=tirati_2punti+1;
		 else if(Stato_bottone_3punti==1) tirati_3punti=tirati_3punti+1;
		 iImposed=1;
	}
	
	if (iState==5){
		//Qui azzero le stats e torno in idle
		tirati_2punti = 0;
		tirati_3punti = 0;
		realizzati_2punti = 0;
		realizzati_3punti = 0;
		
		 iImposed=0;//alla fine ritorno allo stato di idle
	}
    
    
	if (iState>=0 && iState<5){ //forse e meglio entrare qui anche in zero così per mod a obbiettivo 
	//dopo che passo ultimo passaggio torno in zero aspetto qualche secondo il canestro e poi azzero le stat
		//Conteggio Statistiche e le invio
		Serial.println("- Tengo le statistiche e le invio -");
		if(distance_realizzati < 15){
			if(Stato_bottone_2punti==1) realizzati_2punti=realizzati_2punti+1;
		    else if (Stato_bottone_3punti==1) realizzati_3punti=realizzati_3punti+1;
		}
		 
		 if(Stato_bottone_2punti==1){
			 Serial.write(0xff); //flag di inizio pacchetto
			 Serial.write(0x03); //qua dico quanti dati invio in questo caso 2 (0x01 starebbe per 1)
			 Serial.write((char)(2));  //indico la posizione del tiro
			 Serial.write((char)(tirati_2punti)); //non so se serve il casting a char o meno  
			 Serial.write((char)(realizzati_2punti)); 
			 Serial.write(0xfe); //flag di fine pacchetto
			} else if (Stato_bottone_3punti){
				Serial.write(0xff); //flag di inizio pacchetto
				Serial.write(0x03); //qua dico quanti dati invio in questo caso 2 (0x01 starebbe per 1)
				Serial.write((char)(3));  //indico la posizione del tiro
				Serial.write((char)(tirati_3punti)); //non so se serve il casting a char o meno  
				Serial.write((char)(realizzati_3punti)); 
				Serial.write(0xfe); //flag di fine pacchetto
			}
		
	}
	//delay(500);
}
