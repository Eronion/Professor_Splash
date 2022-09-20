import serial
import serial.tools.list_ports
import requests
import time
# import numpy as np

ADAFRUIT_IO_USERNAME = "Eronion"
ADAFRUIT_IO_KEY = "aio_CtXf43ogyYT4rlEb5OQ5nuVywe1y"


class BridgeSparapalloni:

    def setupSerial(self):
        # open serial port
        self.ser = None
        print("list of available ports: ")

        ports = serial.tools.list_ports.comports()
        self.portname=None
        for port in ports:
            print(port.device)
            print(port.description)
            if 'arduino' in port.description.lower():
                self.portname = port.device
        print ("connecting to " + self.portname)

        try:
            if self.portname is not None:
                self.ser = serial.Serial(self.portname, 9600, timeout=0)
        except:
            self.ser = None

        # self.ser.open()

        # internal input buffer from serial
        self.inbuffer = []

# Setup ------------------------------------------------------
    def setup(self):

        self.setupSerial()

# Loop -->In questo loop infinito definisco come raccogliere i dati che mi arrivano dalla seriale
    #      e come gestire l'accesso e l'invio alla seriale dei dati che mi arrivano
    def loop(self):
        print('SPARAPALLONI attiva')
        # infinite loop for serial managing
        lasttime = time.time()
        while (True):
            # look for a byte from serial
            if not self.ser is None:

                if self.ser.in_waiting > 0:
                    # data available from the serial port
                    lastchar = self.ser.read(1)

                    if lastchar == b'\xfe':  # EOL
                        print("\nValue received")
                        self.useData()
                        self.inbuffer = []
                    else:
                        # append
                        self.inbuffer.append(lastchar)

            ts = time.time()
            if ts-lasttime > 0.200:  # ogni 200 millesimi controllo i feed

                feedname_status = 'status'  # Questo sarà il mio feed per l'ON e OFF
                headers_status = {'X-AIO-Key': ADAFRUIT_IO_KEY}
                url_status = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data/last'.format(ADAFRUIT_IO_USERNAME,
                                                                                           feedname_status)
                print(url_status)
                myGET_status = requests.get(url_status, headers=headers_status)
                responseJsonBody = myGET_status.json()
                val_status = responseJsonBody.get('value', None)
                print(val_status)
                # Ricevuto il valore lo invio direttamente alla seriale se devo altrimenti faccio altre cose
                # self.ser.write(b'ON') dovessi inviare un stringa voglio che sia inviata non come stringa ma come
                # byte in ASCII e per questo precedo con la b.
                self.ser.write(val_status.encode())

                if val_status == 1:
                    feedname_program = 'program'  # Questo sarà il mio feed per l'ON e OFF
                    headers_program = {'X-AIO-Key': ADAFRUIT_IO_KEY}
                    url_program_last = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data/last'.format(ADAFRUIT_IO_USERNAME,
                                                                                                     feedname_program)
                    url_program_previous='https://io.adafruit.com/api/v2/{}/feeds/{}/data/last'.format(ADAFRUIT_IO_USERNAME,
                                                                                                       feedname_program)
                    print(url_program_last)
                    myGET_program_last = requests.get(url_program_last, headers=headers_program)
                    responseJsonBody_last = myGET_program_last.json()
                    val_program_last = responseJsonBody_last.get('value', None)

                    myGET_program_previous = requests.get(url_program_previous, headers=headers_program)
                    responseJsonBody_previous = myGET_program_previous.json()
                    val_program_previous = responseJsonBody_previous.get('value', None)
                    print(val_program_previous)
                    if val_program_last != val_program_previous:
                        if val_program_last == 1:
                            self.Tiro_in_loop()
                        elif val_program_last == 2:
                            self.Sfida_di_tiro()

                lasttime = time.time()

# useData -->Qui devo definire come usare i dati che mi arrivato dall'arduino
    def useData(self):
        # I have received a line from the serial port. I can use it
        if len(self.inbuffer) < 3:  # at least header, size, footer
            return False
        # split parts
        if self.inbuffer[0] != b'\xff':
            return False

        numval = int.from_bytes(self.inbuffer[1], byteorder='little')
        if numval>1:
            # uso solo il primo valore
            posizione_tiro = int.from_bytes(self.inbuffer[2], byteorder='little')

            # uso solo il primo valore
            realizzati = int.from_bytes(self.inbuffer[3], byteorder='little')

            # uso solo il primo valore
            tirati = int.from_bytes(self.inbuffer[4], byteorder='little')

            # printo i dati
            strval = "Siamo a  %d su %d da %d punti" % (realizzati, tirati, posizione_tiro)
            print(strval)

            # prendo i dati ricevuti e li posto ad adafruit
            mypostdata1 = {'value': tirati}
            feedname1 = ''
            if posizione_tiro == 3:
                feedname1 = 'tirati3'
            else:
                feedname1 = 'tirati2'
            headers1 = {'X-AIO-Key': ADAFRUIT_IO_KEY}
            url1 = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data'.format(ADAFRUIT_IO_USERNAME, feedname1)
            print (url1)
            myPOST1 = requests.post(url1, data=mypostdata1, headers=headers1)
            print(myPOST1.json())

            mypostdata2 = {'value': realizzati}
            feedname2 = ''
            if posizione_tiro == 3:
                feedname2 = 'realizzati3'
            else:
                feedname2 = 'realizzati2'
            headers2 = {'X-AIO-Key': ADAFRUIT_IO_KEY}
            url2 = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data'.format(ADAFRUIT_IO_USERNAME, feedname2)
            print (url2)
            myPOST2 = requests.post(url2, data=mypostdata2, headers=headers2)
            print(myPOST2.json())

    def Tiro_in_loop(self):
        qualcosa=''

    def Sfida_di_tiro(self):
        qualcosa=''


if __name__ == '__main__':
    br = BridgeSparapalloni()
    br.setup()
    br.loop()


