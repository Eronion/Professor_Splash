import requests
import time

ADAFRUIT_IO_USERNAME = "Eronion"
ADAFRUIT_IO_KEY = "aio_CtXf43ogyYT4rlEb5OQ5nuVywe1y"


class AiSparapalloni:

    #  Loop -->In questo loop infinito definisco come raccogliere i dati dai feed
    #          e come rispondere ad essi con comandi inviati ad altri feed
    def loop(self):
        # infinite loop for serial managing
        self.Inizializzazione()
        lasttime = time.time()
        while True:

            if time.time() - lasttime > 2:  # ogni due secondi
                val_program_last = self.Get_feed('program')

                if val_program_last == 3:
                    self.Tiro_in_loop()
                elif val_program_last == 4:
                    self.Tiro_ad_obbiettivo()
                elif val_program_last == 5:
                    self.Adattiva()

                lasttime = time.time()

    def Tiro_in_loop(self):
        print('tiro a loop')
        self.Post_feed('status', 1)

        while self.Get_feed('program') == 3 and self.Get_feed('status') == 1:
            print("rimango in loop")

        self.Post_feed('status', 0)
        print("Chiudo tiro a loop")

    def Tiro_ad_obbiettivo(self):
        print('Tiro ad obbiettivo')
        obbiettivo = self.Get_feed('obbiettivo')
        serie_completate = 0
        time_loop = time.time()
        self.Post_feed('status', 1)  # avvio macchina

        while self.Get_feed('program') == 4:
            if time.time() - time_loop > 2: # Devo rallenatre i loop altrimenti le richieste ai feed sono troppe
                tirati2 = self.Get_feed('tirati2')
                tirati3 = self.Get_feed('tirati3')
                if tirati2 == 10:
                    self.Post_feed('status', 2)  # cancello le statistiche della macchina e la metto in idle
                    # controlla che non sia questo azzeramento che causa quella scrittura dei valori come 0
                    realizzati2 = self.Get_feed('realizzati2')
                    if realizzati2 >= obbiettivo:
                        serie_completate = serie_completate + 1
                        self.Post_feed('serie', serie_completate)
                    self.Azzera_statistiche(2)
                    self.Post_feed('status', 1)  # riavvio macchina
                elif tirati3 == 10:
                    realizzati3 = self.Get_feed('realizzati3')
                    if realizzati3 >= obbiettivo:
                        serie_completate = serie_completate + 1
                        self.Post_feed('serie', serie_completate)
                    self.Azzera_statistiche(3)
                    self.Post_feed('status', 1)  # riavvio macchina
        self.Post_feed('status', 0)

        # Valuta se migliorare il tiro ad obbiettivo non fermando la macchina e poi facendola ripartire per controllare
        # se gli obbiettivi sono stati raggiunti. Potresti solo azzerare le stats della macchina ma farla continuare
        # per farlo devi implementare questa cosa anche nella macchina che per ora azzera e si ferma ma potresti molto
        # facilmente fare in modo che cancella e ritorna in loop

    def Adattiva(self):  # DA DEFINIRE
        print('adattiva')
        livello = self.Get_feed('livello')
        serie_completate = 0
        serie_di_fila = 0
        time_loop = time.time()
        self.Post_feed('status', 1)
        while self.Get_feed('program') == 5:
            if time.time() - time_loop > 2:
                tirati2 = self.Get_feed('tirati2')
                tirati3 = self.Get_feed('tirati3')
                if tirati2 == 10:
                    self.Post_feed('status', 2)  # cancello le statistiche della macchina e la metto in idle
                    realizzati2 = self.Get_feed('realizzati2')
                    if realizzati2 >= livello:
                        serie_di_fila = serie_di_fila + 1
                        serie_completate = serie_completate + 1
                        self.Post_feed('serie', serie_completate)
                        if serie_di_fila >= 2:
                            livello = livello + 1
                            serie_di_fila = 0
                    else:
                        serie_di_fila = 0
                    self.Azzera_statistiche(2)
                    self.Post_feed('status', 1)
                elif tirati3 == 10:
                    realizzati3 = self.Get_feed('realizzati3')
                    if realizzati3 >= livello:
                        serie_di_fila = serie_di_fila + 1
                        serie_completate = serie_completate + 1
                        self.Post_feed('serie', serie_completate)
                        if serie_di_fila >= 2:
                            livello = livello + 1
                            self.Post_feed('livello', livello)
                            serie_di_fila = 0
                    else:
                        serie_di_fila = 0
                    self.Azzera_statistiche(3)
                    self.Post_feed('status', 1)
        self.Post_feed('status', 0)

        # Un'idea per ridurre le get ai feed sarebbe di non fare insieme e prima le get a tirati da 2 e da 3 ma di
        # farne prima una e vedere se e maggiore di 10 e solo else fare l'altra

    def Inizializzazione(self):

        self.Post_feed('program', 0)
        self.Post_feed('tirati2', 0)
        self.Post_feed('tirati3', 0)
        self.Post_feed('realizzati2', 0)
        self.Post_feed('realizzati3', 0)
        self.Post_feed('serie', 0)

    def Azzera_statistiche(self, posizione):
        if posizione == 2:
            self.Post_feed('tirati2', 0)
            self.Post_feed('tirati3', 0)
        elif posizione == 3:
            self.Post_feed('realizzati2', 0)
            self.Post_feed('realizzati3', 0)

    def Get_feed(self, feedname):
        headers = {'X-AIO-Key': ADAFRUIT_IO_KEY}
        url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data/last'.format(ADAFRUIT_IO_USERNAME, feedname)
        myGET = requests.get(url, headers=headers)
        responseJsonBody = myGET.json()
        str_val = responseJsonBody.get('value', None)
        time.sleep(1)
        return int(str_val)

    def Post_feed(self, feedname, valore):
        mypostdata = {'value': valore}
        headers = {'X-AIO-Key': ADAFRUIT_IO_KEY}
        url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data'.format(ADAFRUIT_IO_USERNAME, feedname)
        myPOST = requests.post(url, data=mypostdata, headers=headers)
        print(myPOST.json())
        time.sleep(1)

        #  ACHTUNG!!!  get dal feed ti torna una stringa


if __name__ == '__main__':
    ai = AiSparapalloni()
    ai.loop()
