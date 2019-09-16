
import threading
#import socket
import numpy
import time
from queue import Queue
import RPi.GPIO as GPIO
from bluetooth import *


class valvepiSend(threading.Thread):

    def __init__(self,sock):

        threading.Thread.__init__(self)
        self.sock = sock



    def run(self):

        time.sleep(50)

    #벨브 상태를 알려주는 함수.

    def sendState(self,valveNumber=None,state=None):

        self.sock.send(encodeServer('valvepi/{}/{}'.format(valveNumber,state)))







class valvepiRecv(threading.Thread):
    valvepiSend
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.queue = Queue()
        self.valve01 = True
        self.valve02 = True
        self.valve03 = True
        self.valve04 = True
        self.deelay = 8

        #self.backup = ['B8_27_EB_C5_1C_CA','B8_27_EB_7F_74_AA','B8_27_EB_97_BD_87','B8_27_EB_35_AB_D8']
        self.location = ['B8_27_EB_C5_1C_CA','B8_27_EB_7F_74_AA','B8_27_EB_97_BD_87','B8_27_EB_35_AB_D8']

        '''
            'B8_27_EB_C5_1C_CA': 'A'
            'B8_27_EB_7F_74_AA': 'B'
            'B8_27_EB_97_BD_87': 'C'
            'B8_27_EB_35_AB_D8': 'D'
            '''

        #self.manual_1 = False
        #self.manual_2 = False
        #self.manual_3 = False
        #self.manual_4 = False
        #사용자 수동 자동 모드드
        self.manual = False
 


        self.ValveGPIO = [12,13,18,19]
        #GPIO의 경고 메세지가 안뜨게 변경
        GPIO.setwarnings(False)
        #GPIO를 정리
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        #ValveGPIO에 있는 리스트의 요소들을 전부다
        #GPIO.OUT형태로 변환
        GPIO.setup(self.ValveGPIO, GPIO.OUT)

        #초기 Valve들의 상태를 닫힌 상태로 만든다.
        GPIO.output(self.ValveGPIO[0], True)
        GPIO.output(self.ValveGPIO[1], True)
        GPIO.output(self.ValveGPIO[2], True)
        GPIO.output(self.ValveGPIO[3], True)



        #켜지는 모드


    #'server/valveCompare/{}/{}'.format(self.address,compare_value)

    def run(self):
    #쓰레드 실행시 작동되는 영역
        

        while True:


                #lock.acquire()
                data = sock.recv(1024).decode('utf-8')
                #데이터를 받아오는데 버퍼의 크기는 1024bit
                #utf-8로 디코딩

                #데이터가 들어올떄 큐에 넣어서 하나씩 처리를 한다.
                self.queue.put(data)
                print(data)

                data=self.queue.get()
                #'/'을 기준으로 문자열을 파싱해서 문자들 를 처리한다.
                data = data.split('/')
                if data[0] == 'server':
                    if data[1] =='valvepi':
                        print(self.manual)

                        
                        if self.manual:

                            if data[2] == 'valve01':
                                # 벨브 1번이 켜지는 구문
                                if data[3] == 'on':
                                    #valve01의 상태를 바꿔준다.
                                    self.valve01 = False
                                    #벨브의 상태가 변했을때 서버로 벨브의 상태를 보낸다.
                                    #벨브1 번의 상태가 켜졌다. 꺼졌을때는 0번으로 보낸다.
                                    #나머지 구문들도 같다.
                                    self.sendValveState(valvenumber=1,state=1)
                                    #벨브1번이 켜진다.
                                    GPIO.output(self.ValveGPIO[0],False)


                                # 벨브 1번이 꺼지는 구문
                                elif data[3] == 'off':
                                
                                    self.valve01 = True
                                    self.sendValveState(valvenumber=1, state=0)
                                    GPIO.output(self.ValveGPIO[0], True)
                                    
                            elif data[2] == 'valve02':

                                if data[3] == 'on':
                                   
                                    self.valve02 = False

                                    self.sendValveState(valvenumber=2, state=1)
                                    GPIO.output(self.ValveGPIO[1], False)
                                elif data[3] == 'off':
                                
                                    self.valve02 = True
                                    self.sendValveState(valvenumber=2, state=0)
                                    GPIO.output(self.ValveGPIO[1], True)
                            elif data[2] == 'valve03':

                                if data[3] == 'on':
                                    
                                    self.valve03 = False

                                    self.sendValveState(valvenumber=3, state=1)
                                    GPIO.output(self.ValveGPIO[2], False)
                                elif data[3] == 'off':
                                   
                                    self.valve03 = True
                                    self.sendValveState(valvenumber=3, state=0)
                                    GPIO.output(self.ValveGPIO[2], True)
                            elif data[2] == 'valve04':

                                if data[3] == 'on':
                                    
                                    self.valve04 = False

                                    self.sendValveState(valvenumber=4, state=1)
                                    GPIO.output(self.ValveGPIO[3], False)
                                elif data[3] == 'off':
                                    
                                    self.valve04 = True
                                    self.sendValveState(valvenumber=4, state=0)
                                    GPIO.output(self.ValveGPIO[3], True)

                    elif data[1] == 'valveCompare':
                        #서버에서 사용자 토양습도값과 센서의 값들을 서버에서 비교를 하여
                        #보내주는 값이다. 이떄 센서의 주소가 함께 보내지는데 이 주소를 통해서
                        #지역을 찾는다.
                        print('valveCompare')
                        #만약 GUI에서 수동모드일때 작동을 안한다.
                        if not self.manual:
                            for i,address in enumerate(self.location):
                                print(address == data[2])
                                print(data[2])
                                if address == data[2] :

                                    self.locationFind(i,command='on')
                    elif data[1] == 'valveStop':
                        # 서버에서 사용자 토양습도값과 센서의 값들을 서버에서 비교를 하여
                        # 보내주는 값이다. 이떄 센서의 주소가 함께 보내지는데 이 주소를 통해서
                        # 지역을 찾는다.
                        print('valveStop')
                        # 만약 GUI에서 수동모드일때 작동을 안한다.
                        if not self.manual:
                            for i,address in enumerate(self.location):
                                print(address == data[2])
                                print(data[2])
                                if address == data[2]:

                                    self.locationFind(i,command='off')
                    elif data[1] =='custum':
                        #벨브가 자동모드에서 수동모드로 변환을 해준다.
                        if data[2] =='manual':
                            self.manual = True
                            #변환된 상태를 서버측으로 다시보낸다.
                            self.sock.send(encodeServer('valvepi/valvecustum/manual'))
                        #벨브의 수동모드에서 자동모드로 변환해준다.
                        elif data[2] =='auto':
                            self.manual = False
                            # 변환된 상태를 서버측으로 다시보낸다.
                            self.sock.send(encodeServer('valvepi/valvecustum/auto'))
                           

                    elif data[1] =='valvepi2':
                        #벨브파이가 켜져있는 상태에서 GUI가 접속을 하면
                        #GUI에서 벨브상태가 어떤지에 대해서 서버측에 요청을 하고
                        #서버는 다시 그 요청을 벨브한테 알려준다.
                        #요청을 받은 벨브파이는 다시 서버측으로 현재 벨브들의 상태를 보낸다.
                        if data[2] =='allrequest':


                           self.sock.send(encodeServer('valvepi/displaypi/ar/1#{}#2#{}#3#{}#4#{}'.format(int(self.valve01),int(self.valve02),int(self.valve03),int(self.valve04))))





        # if data[0] == 'valvepi':
        #     if data[1] == '1' : #임시적인 벨브번호
        #         if data[2] == 'command':
        #             if data[3] ==   '1':
        #                 pass #여기서는 벨브가 켜진다.
        #
        # if data[0] == 'valvepi':
        #     if data[1] == '1':  # 임시적인 벨브번호
        #         if data[2] == 'command':
        #             if data[3] == '0':
        #                 pass #여기서는 벨브가 꺼진다.

        # print(data)

        # lock.release()
    def locationFind(self,number,command):
        #벨브의 자동으로 될떄 어디 센서가 값들이 원하는지가 필요할때
        #그 위치를 찾는데 사용되는 함수.
        print('locationFind')
        if command == 'on':

            if number == 0 :
                self.valve01=False
                self.sendValveState(valvenumber=1,state=1)
                GPIO.output(self.ValveGPIO[0], False)
            elif number ==1 :
                self.valve02=False
                self.sendValveState(valvenumber=2, state=1)
                GPIO.output(self.ValveGPIO[1], False)
            elif number == 2 :
                self.valve03=False
                self.sendValveState(valvenumber=3, state=1)
                GPIO.output(self.ValveGPIO[2], False)

            elif number ==3 :
                self.valve04=False
                self.sendValveState(valvenumber=4, state=1)
                GPIO.output(self.ValveGPIO[3], False)
        elif command =='off':

            if number == 0 :
                self.valve01 = True
                self.sendValveState(valvenumber=1, state=0)
                GPIO.output(self.ValveGPIO[0], True)
            elif number ==1 :
                self.valve02 = True
                self.sendValveState(valvenumber=2, state=0)
                GPIO.output(self.ValveGPIO[1], True)
            elif number == 2 :
                self.valve03 = True
                self.sendValveState(valvenumber=3, state=0)
                GPIO.output(self.ValveGPIO[2], True)

            elif number ==3 :
                self.valve04 = True
                self.sendValveState(valvenumber=4, state=0)
                GPIO.output(self.ValveGPIO[3], True)

    def turnOnValve(self,position=None,time=None):
        #벨브를 키고 끄는 함수
        #만들기는 했지만 사용을 하진않았음
        print('turnOn')
        if position == 1:
            self.valve01 = True
            time.sleep(time)
            self.valve01 = False
        elif position == 2:
            self.valve02 = True
            time.sleep(time)
            self.valve01 = False
        elif position == 3:
            self.valve03 = True
            time.sleep(time)
            self.valve01 = False
        elif position == 4:
            self.valve04 = True
            time.sleep(time)
            self.valve01 = False

    def sendValveState(self,valvenumber=None,state = None):
    #벨브의 상태를 서버에게 보내는 함수

            self.sock.send(encodeServer('valvepi/valvestate/{}/{}'.format(valvenumber,state)))
            
    def sendValveCustum(self,custum):
    #벨브의 상태를 서버측에 보내는 함수.
            if custum == 'auto':
                self.sock.send(encodeServer('valvepi/custum/auto'))
            elif custum == 'manual':
                self.sock.send(encodeServer('valvepi/custum/manual'))
                

def encodeServer(strk):
#encoding떄 사용되는 함수.
    strk = str(strk)
    a = strk.encode('utf-8')
    return a






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

    #서버 전송용 Thread생성
    valvepiSend = valvepiSend(sock)
    #서버 수신용 Trhead생성
    valvepiRecv = valvepiRecv(sock)


    valvepiSend.start()
    valvepiRecv.start()

