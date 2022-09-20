import requests
import time
# import numpy as np

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

            ts = time.time()
            if ts-lasttime > 0.5:  # ogni mezzo secondo

                val_status = self.Get_feed('status')
                if val_status == 1:
                    #  print("Status 1")
                    feedname_program = 'program'  # Questo sarà il mio feed per l'ON e OFF
                    headers_program = {'X-AIO-Key': ADAFRUIT_IO_KEY}

                    url_program_previous = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data/previous'.format(ADAFRUIT_IO_USERNAME, feedname_program)
                    print(url_program_previous)
                    myGET_program_previous = requests.get(url_program_previous, headers=headers_program)

                    responseJsonBody_previous = myGET_program_previous.json()
                    str_val_program_previous = responseJsonBody_previous.get('value', None)
                    val_program_previous = int(str_val_program_previous)

                    val_program_last = self.Get_feed('program')

                    print(str_val_program_previous + "<->" + str(val_program_last))
                    if val_program_last != val_program_previous:
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
        self.Post_feed('status', 1)
        while self.Get_feed('program') == 4:
            tirati2 = self.Get_feed('tirati2')
            tirati3 = self.Get_feed('tirati3')
            if tirati2 == 10:
                realizzati2 = self.Get_feed('realizzati2')
                if realizzati2 >= obbiettivo:
                    serie_completate = serie_completate + 1
                    self.Post_feed('serie', serie_completate)
                self.Azzera_statistiche()
            elif tirati3 ==10:
                realizzati3 = self.Get_feed('realizzati3')
                if realizzati3 >= obbiettivo:
                    serie_completate = serie_completate + 1
                    self.Post_feed('serie', serie_completate)
                self.Azzera_statistiche()
        self.Post_feed('status', 0)

    def Adattiva(self): # DA DEFINIRE
        print('adattiva')
        livello = self.Get_feed('livello')
        serie_completate = 0
        serie_di_fila = 0
        self.Post_feed('status', 1)
        while self.Get_feed('program') == 5:
            tirati2 = self.Get_feed('tirati2')
            tirati3 = self.Get_feed('tirati3')
            if tirati2 == 10:
                realizzati2 = self.Get_feed('realizzati2')
                if realizzati2 >= livello:
                    serie_di_fila = serie_di_fila + 1
                    serie_completate = serie_completate + 1
                    self.Post_feed('serie', serie_completate)
                    if serie_di_fila >= 2:
                        livello=livello+1
                        serie_di_fila = 0
                else:
                    serie_di_fila = 0
                self.Azzera_statistiche()
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
        self.Post_feed('status', 0)

    def Inizializzazione(self):

        self.Post_feed('program', 0)
        self.Post_feed('tirati2', 0)
        self.Post_feed('tirati3', 0)
        self.Post_feed('realizzati2', 0)
        self.Post_feed('realizzati3', 0)

    def Azzera_statistiche(self):
        self.Post_feed('tirati2', 0)
        self.Post_feed('tirati3', 0)
        self.Post_feed('realizzati2', 0)
        self.Post_feed('realizzati3', 0)


    def Get_feed(self, feedname):
        headers = {'X-AIO-Key': ADAFRUIT_IO_KEY}
        url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data/last'.format(ADAFRUIT_IO_USERNAME, feedname)
        myGET = requests.get(url, headers=headers)
        responseJsonBody = myGET.json()
        str_val = responseJsonBody.get('value', None)
        time.sleep(60)
        return int(str_val)

    def Post_feed(self, feedname, valore):
        mypostdata = {'value': valore}
        headers = {'X-AIO-Key': ADAFRUIT_IO_KEY}
        url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data'.format(ADAFRUIT_IO_USERNAME, feedname)
        myPOST = requests.post(url, data=mypostdata, headers=headers)
        # print(myPOST.json())
        time.sleep(60)

        #  ACHTUNG!!!  get dal feed ti torna una stringa


if __name__ == '__main__':
    ai = AiSparapalloni()
    ai.loop()


