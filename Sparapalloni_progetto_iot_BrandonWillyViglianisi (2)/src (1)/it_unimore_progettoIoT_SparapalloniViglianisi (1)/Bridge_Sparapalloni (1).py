import serial
import serial.tools.list_ports
import requests
import time
# import numpy as np

ADAFRUIT_IO_USERNAME = "Eronion"
ADAFRUIT_IO_KEY = "aio_CtXf43ogyYT4rlEb5OQ5nuVywe1y"


class BridgeSparapalloni():
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
            if ts-lasttime > 0.250:  # ogni 250 millesimi controllo i feed

                feedname = 'status'  # Questo sarà il mio feed per l'ON e OFF
                headers = {'X-AIO-Key': ADAFRUIT_IO_KEY}
                url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data/last'.format(ADAFRUIT_IO_USERNAME, feedname)
                print(url)
                myGET = requests.get(url, headers=headers)
                responseJsonBody= myGET.json()
                val = responseJsonBody.get('value',None)
                print(val)
                # Ricevuto il valore lo invio direttamente alla seriale
                # self.ser.write(b'ON') dovessi inviare un stringa voglio che sia inviata non come stringa ma come byte in ASCII e per questo precedo con la b
                self.ser.write(val)
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
            i=0
            val = int.from_bytes(self.inbuffer[i + 2], byteorder='little')
            strval = "Sensor %d: %d " % (i, val)
            print(strval)

            #prendo il dato ricevuto e lo posto ad adafruit, potrei anche trasformarlo prima in base alle mie esigenze
            mypostdata = {'value': val}
            feedname = 'sensor'
            headers = {'X-AIO-Key': ADAFRUIT_IO_KEY}
            url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data'.format(ADAFRUIT_IO_USERNAME,feedname)
            print (url)
            myPOST = requests.post(url, data=mypostdata, headers=headers)
            print(myPOST.json())


if __name__ == '__main__':
    br = BridgeSparapalloni()
    br.setup()
    br.loop()


