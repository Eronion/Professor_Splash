# Professor_Splash

![image](https://user-images.githubusercontent.com/62468674/191198780-45e2e347-1de3-46f4-a121-9f550f8bb399.png)

# Abstract

L’idea di base è di prototipare una macchina spara palloni per il basket, utilizzabile per passare la palla ad un atleta permettendogli così di svolgere sessioni di tiro maggiormente produttive. Il vantaggio rispetto alle macchine attualmente presenti sul mercato sarebbe quello di tenere anche delle precise statistiche su cui effettuare, tramite algoritmi di machine learning, predizioni mirate al miglioramento della performance al tiro del singolo atleta.

(Per un’idea sul funzionamento delle macchine già presenti sul mercato si veda:  https://youtu.be/SpDcDpvmWLw?t=38 )


# Parte Thing (Prototipazione Arduino + Sensori ed attuatori)
Verrà utilizzato il microcontrollore Arduino per l’implementazione di un loop di controllo che agisca in due direzioni principali:
1.	Tramite l’ausilio di attuatori e sensori ricevere e correttamente passare la palla ad un atleta;
2.	Tenere le statistiche circa la sessione considerando anche la posizione da cui il cestista tira, grazie ad esempio a sensori di pressione posti nel pavimento. Tutti i dati raccolti dovranno essere comunicati tramite seriale ad un bridge che si occuperà della trasmissione dei dati. 

# Parte Internet (Bridge più comunicazione con server)
Implementato il bridge (in Python) e scelto un protocollo di comunicazione (MQTT o HTPP) l’obbiettivo di questo progetto è di costruire lato server un database delle sessioni di tiro da poter sfruttare nella successiva fase. Potresti implementare anche questo lato con telegram andando a definire dei comandi da scambiare con il controllore che farà la parte di un bot. Ad esempio mi può inviare statistiche ed io per iniziare una sessione di tiro posso mandargli un comando in cui dico chi sono così da identificare a chi assegnare quelle statistiche.

# Parte Machine Learning (Utilizzo dei dati ottenuti)
L’ultimo passo prevede l’utilizzo di tecniche proprie del machine learning per l’analisi della correlazione tra canestri realizzati in allenamento e canestri realizzati in partita da un cestista. Quantificando il legame che intercorre tra queste due misure saremo in grado di consigliare ad ogni atleta il numero ideali di tiri da effettuare in allenamento così da poter migliorare le proprie prestazioni durante le partite.


