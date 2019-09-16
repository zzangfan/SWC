import threading
#Thread 모듈
from bluetooth import *
#블루투스 접속시 사용되는 모듈
import numpy as np
#수학적 계산을 할시 사용되는 모듈
from datetime import datetime
#시간을 사용하기 위한 모듈
from queue import Queue
#데이터를 하나씩 처리하기위한 큐
import smbus
#Lux 센서를 위한 모듈
import spidev, time
#토양습도를 측정하기 위해 analog -> digital 변환시 사용되는 모듈
import Adafruit_DHT
#온도, 습도 얻기 위한 센서 모듈
import time


class sensorPiSend(threading.Thread): #센서파이가 메인서버로 보내는 용도

    def __init__(self,sock):
        threading.Thread.__init__(self)
        # self.sock = sock
        self.queue = Queue()
        self.sending_time = 0
        self.daemon = False
        self.DEVICE = 0x23
        self.POWER_DOWN = 0x00
        self.POWER_ON = 0x01
        self.RESET = 0x07
        self.ONE_TIME_HIGH_RES_MODE = 0x20

        self.bus = smbus.SMBus(1)
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)

        self.solidChannel = 1
        self.sleepTime = 1
        self.spi.max_speed_hz = 1000000
        self.pin = 14
        self.sensor = Adafruit_DHT.DHT11
        print('#02')

        def sensorDataList(self):
            # humidity, temperature dht11
            self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
            #습도, 온도
            self.solid_level = self.ReadChannel(self.solidChannel)
            self.solid_volts = self.ConvertVolts(self.solid_level)
            #토양습도
            self.Lux = self.readLight()
            #조도
            #안전을 위한 형변환을 한다.
            self.humidity= int(float(self.humidity))
            self.temperature = int(float(self.temperature))
            self.solid_volts = int(float(self.solid_volts))
            self.Lux = int(float(self.Lux))


            return self.humidity, self.solid_volts, self.temperature, self.Lux

    def run(self):
        while True:

            while True:
                sensorData = self.sensorDataList()
                self.sock.send(encodeStr(
                    makeSensordata(humidity=sensorData[0], solidHumidty=sensorData[1], temperature=sensorData[2],
                                   light=sensorData[3])))
                time.sleep(3)
                print('working')

    def setTime(self,int):

        self.sending_time = int


    def testData(self):

        return np.random.randint(1,50)

    def convertToNumber(self, data):
        #숫자로 변환
        return ((data[1] + (256 * data[0])) / 1.2)

    def readLight(self):
        #빛을 읽어서LUX값을 보옂ㄴ다.
        data = self.bus.read_i2c_block_data(self.DEVICE, self.ONE_TIME_HIGH_RES_MODE)
        return self.convertToNumber(data)

    def ReadChannel(self, channel):
        #아날로그 값을 디지털로 바꾸기 위해 사용되는 함수
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def ConvertVolts(self, data):
        # 아날로그 값을 디지털로 바꾸기 위해 사용되는 함수
        volts = ((data / float(1023))) * 100

        return volts


class sensorPiRecv(threading.Thread): #센서파이 받는 용도


    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.queue = Queue()
        self.POP_From_Server = None
        self.T3H_data_From_Server = None
        self.REH_data_From_Server =None
        self.daemon=False

    def run(self):
        while True:

            data = self.sock.recv(1024).decode('utf-8')
            #데이터를 받아 decoding을 한후
            #큐에 넣어서 하나씩 처리한다.
            self.queue.put(data)
            data = self.queue.get()
            data = data.split('/')
            if data[0] == 'server':

                if data[1] == 'weather':
                #기상청에서 받은 데이터
                    self.POP_From_Server,self.T3H_data_From_Server,self.REH_data_From_Server=int(data[2].split(','))


    def getPOP_From_Server(self):
        #강수확률 함수
        return self.POP_From_Server





testing = 1


def makeSensordata(humidity=None,temperature=None,solidHumidty=None,light=None):
    #4개의 속성 습도,온도,토양습도,조도센서
    #센서에서 얻은 데이터를 보내주기 위해 만든 함수
    global testing
    testing += 1
    none_defaulti =  testing #"-1"

    base_str = 'sensorpi/sensordata/'
    if humidity == None:
        humidity = none_defaulti
    if temperature ==None:
        temperature = none_defaulti

    if solidHumidty ==None:
        solidHumidty =none_defaulti
    if light ==None:
        light = none_defaulti
    else:
        pass
    humidity = str(humidity)
    temperature = str(temperature)
    solidHumidty = str(solidHumidty)
    light = str(light)
    nowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sensor_data ="{}{}%{}%{}%{}%{}".format(base_str,nowTime,humidity,temperature,solidHumidty,light)


    return sensor_data








def encodeStr(str):

    str = str.encode('utf-8')
    return str

def decodeStr(str):

    str=str.decode('utf-8')
    return str





if __name__ == "__main__":
    host = 'B8:27:EB:D0:AA:C5'
    #포트주소 블루투스는 0~100번대의 포트가 존재한다.
    port = 2
    #host = 'localhost'
    #port = 1803
    while True:
        try:
            #블루투스를 RFCOMM방식으로 요청한다.
            sock = BluetoothSocket(RFCOMM)
            #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            #동기화를 위한 Thread의 락이다
            #락을 얻은 쓰레드는 우선권을 얻어
            #다른 쓰레드들이 기다리고 락을 얻은
            #쓰레드만 사용이 가능하다.
            lock = threading.Lock()
            #접속이 성공적으로 되면 loop에서 빠져나간다.
            break

        #만약 접속실패시 재접속을 한다.
        except ConnectionRefusedError:
            time.sleep(2)
            pass


    try:
        #센서파이 통신을 위한 쓰레드
        sensorPiRecv=sensorPiRecv(sock)
        sensorPiRecv.start()

        sensorPiSend=sensorPiSend(sock)
        sensorPiSend.start()


        print('#04')
    except KeyboardInterrupt:
        sock.close()
