# ------------------------------------------------------
# ---------------------- gui.py -----------------------
# ------------------------------------------------------


# -*- coding: utf-8 -*-
#copyright:zzangfan
from PyQt5.QtWidgets import *

from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import glob
#폴더안에 파일들을 찾기 위하 모듈
import pandas as pd
#데이터프레임 처리가 쉬운 판단스, 시계열 변환을 위해 사용함
from pandas.plotting import register_matplotlib_converters
from datetime import timedelta
#시간들사이의 값을 뺴고 더하기 위한 모듈
import threading
#쓰레드
import time
#시간 지연 모듈
from queue import Queue
#데이터를 하나씩 처리하기위한 큐
import os
#폴더나 파일을 생성할떄 사용하는 모듈
import sys
#시스템 접근시 필요한 모듈
from bluetooth import *
#블루투스 통신을 위한 모듈

# class command(threading.Thread):
#     global th_list
#     def __init__(self,sock):
#         threading.Thread.__init__(self)
#
#         self.command_pi = ['sensorpi','valvepi']
#         self.command_sensor = ['all','humidity']
#         self.command_common = ['state']
#         self.command_valve = ['turnon','turnoff']
#         self.daemon=True #메인쓰레드가 종류시 종료가 된다.
#         self.defaulPOP = 50 #이값은 초기 강수확률의 값을 입력한다.
#
#
#     def run(self):
#          while True:
#             #  command = input('제어를 원하시는 pi를 입력하세요.(sensorpi or valvepi')
#             #  if command == 'sensorpi':
#             #      pi_kind = command
#             #
#             #      second_comman = input('원하시는 명령어를 입력해주세요.(start of stop)')
#             #      if second_command == 'start':
#             #          pi_command =second_command
#             #      elif second_command == 'stop':
#             #          pi_command = 'stop'
#             #
#             #
#             # elif command =='valvepi':
#             #     self.pi_kind=command
#             # else: print('종류의 맞게 입력해주세요')
#             #     break
#             first_command=self.commandinput('제어를 원하시는 pi를 입력하세요.(sensorpi or valvepi)',self.command_pi)
#             if first_command == 'sensorpi':
#
#                 second_command=self.commandinput('sensorpi의 명령어를 입력하세요.{}'.format(self.command_sensor), self.command_sensor)
#                 if second_command == 'all':
#                     third_command = self.commandinput('센서파이의 상태를 결정해주세요.{}'.format(self.command_common),self.command_common)
#                     if third_command == 'state':
#                         last_command = self.commandinput('상태를 지정해주세요.(0,1)')
#                 if second_command == 'humidity':
#                     third_command = self.commandinput('습도센서를 상태를 결정해주세요.{}'.format(self.command_common),self.command_common)
#                     if third_command == 'state':
#                         last_command = self.commandinput('상태를 지정해주세요.(0,1')
#             if first_command == 'valvepi':
#                 second_command=self.commandinput('valvepi의 명령어를 입력하세요{}'.format(self.command_valve), self.command_valve)
#
#             final_command ='{}/{}/{}/{}'.format(first_command,second_command,third_command,last_command)
#             self.sock.send(final_command)
#
#             sock.send(encodeServer('display/user/defaultPOP/{}'.format(self.defaultPOP))) #사용자가 초기의 원하는 값을 설정할수 있다.
#
#
#     def commandinput(self,inputs, command_list):
#
#
#         while True:
#             input_str = input(inputs).strip()
#
#             for i in command_list:
#
#                 if input_str == str(i):
#                     return str(i)
#                 else:
#                     print('명령어 리스트없는 값입니다.'.format(command_list))
#                     pass
#
#     def setUserKey(self,str): # 유저가 버튼을 눌렀을때 값들을 설정해주는 값이다.
#
#         if str == 'defaultPOP':
#
#             self.defaulPOP = str
#
#         return  self.defaulPOP


class displaySend(threading.Thread):
    #메인 서버에 전송용 클래스
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.daemon = False
        self.queue = Queue()
        

    def sendCommand(self, str):
        #명령어를 보내는 함수
        lock.acquire()
        self.sock.send(encodeServer(str))
        lock.release()
    def sendAR(self):
        #접속시 벨브파이들의 상태를 요청하는 함수
        self.sock.send(encodeServer('displaypi/valvepi/allrequest'))
    def run(self):
       pass
class displayRecv(threading.Thread):
    #수신용 클래스
    global window
    #실시간 그래프 갱신을 위해 사용
    global displaySend
    #명령어를 보내기 위해 선언
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.daemon = False
        self.queue = Queue()
        self.weather_information = [-1, -1, -1]
        self.valvenumber1 = False
        self.valvenumber2 = False
        self.valvenumber3 = False
        self.valvenumber4 = False
        self.true = True
        #수동모드를 위한 변수
        self.manual = False
        
       
        


    def getWeahterInformation(self):
    #메인서버에서 받은 기상청 정보를 얻은 함수
        return self.weather_information

    def run(self):
        
        while True:

            data = self.sock.recv(1024).decode('utf-8')  # utf-8로 인코딩된값을 decoding을한다.
            #데이터를 하나씩 넣고 하나씩 꺼낸다.
            self.queue.put(data)
            get_data = self.queue.get()

            #문자열을 '/'을 사용해서 나눈다.
            get_data = get_data.split('/')
            print(get_data)
            if get_data[0] == 'server':
                if get_data[1] == "display":
                    '''
                    text파일을 이용한 이유는 판다스를 사용해 데이터 프레임을 만든후 처리하는 메모리양을
                    라즈베리파이가 감당히 힘들것 같다는 이유에서 이다.
                    필요한 주소마다 처리를 하는 경우에는 데이터프레임을 만들고 찾고 다시 만드는 것 보다는
                    통신을 할때 그 주소에 맞는 텍스트 파일을 지정한후 그래픽 처리를 해야 더 편할것 같아서 이다.

                    '''
                    print('display')
                    sensordata = get_data[2].split('%')
                    text_name = sensordata[-1].replace('server','')
                    file_check = sensordata[-1].replace('server','')
                    text_name = str(text_name).replace("'", "")
                    text_name = text_name.replace("(", "")
                    text_name = text_name.replace(")", "").strip()
                    sensordata = str(sensordata).replace('[', '')
                    sensordata = str(sensordata).replace(']', '')
                    sensordata = str(sensordata).replace("'", "")
                    sensordata = "{}{}".format(sensordata, '\n')
                    if os.path.isdir('graphs'):
                        pass
                    else:
                        os.makedirs('graphs')

                    with open('graphs/{}.txt'.format(text_name), 'a+t', encoding='utf-8') as dp:

                        dp.writable()
                        dp.write(sensordata)
                    try:

                        file = 'graphs/{}.txt'.format(file_check)
                        print(file == str(window.File))
                        if (file == str(window.File)) and window.image_make:
                            window.update_graph()
                    except NameError:
                        pass


                elif get_data[1] == "weatherInformation":
                    #메인서버에서 받은 기상청 데이터를 처리한다.
                    print("information")
                    self.weather_information = list(map(int, get_data[2].split(',')))

                #'server/valvepi/{}/{}'
                #벨브에서 온 상태를 학인한다.
                #벨브에서 온 상태를 확인하면서 동시에 버튼의 텍스틀 변환을 해준다.
                #여기서 벨브와 GUI간의 통신이 안될시에는 wating이라는 문구가 계속 떠있고
                #통신이 되었을때는 그 상태에 맞게 변환을 해준다.
                elif get_data[1] == 'valvepi':
                    print('#valvepi')
                    if get_data[2] == 'valve01':
                        if get_data[3] == 'on':
                            print('working')
                            self.valvenumber1 = True
                            window.EVController_01.setText('전동벨브01 OFF')
                            # window.processEvents()
                            # QApplication.processEvents()
                        else:
                            self.valvenumber1 =False
                            window.EVController_01.setText('전동벨브01 ON')
                    elif get_data[2] =='valve02':
                        if get_data[3] == 'on':
                            self.valvenumber2 = True
                            window.EVController_02.setText('전동벨브02 OFF')
                        else:
                            self.valvenumber2 = False
                            window.EVController_02.setText('전동벨브02 ON')
                    elif get_data[2] == 'valve03':
                        if get_data[3] == 'on':
                            self.valvenumber3 = True
                            window.EVController_03.setText('전동벨브03 OFF')
                        else:
                            self.valvenumber3 = False
                            window.EVController_03.setText('전동벨브03 ON')
                    else:
                        if get_data[3] == 'on':
                            self.valvenumber4 = True
                            window.EVController_04.setText('전동벨브04 OFF')
                        else:
                            self.valvenumber4 = False
                            window.EVController_04.setText('전동벨브04 ON')

                #GUI가 자동및 수동으로 벨브를 제어를 하고싶을때 사용되는 명령어.
                #만약 자동일때는 벨브들을 키고 끄고를 할수 없다.
                #하지만 수동일떄는 요청이 가능하다 .
                #수동과 자동의 상태의 여부는 버튼에 텍스틀 보면 확인이 가능하다.
                #Auto라고 써져있으면 현재 자동상태인것이다.
                elif get_data[1] =='valvecustum':
                    if get_data[2] =='auto':
                        window.switch_btn.setText('Auto')
                        self.manual = False

                    elif get_data[2] == 'manual':
                        window.switch_btn.setText('Manual')
                        self.manual = True
                elif get_data[1] == 'valvestate':
                     print(get_data)
                     if get_data[2] == '0':
                         if get_data[3] =='0':
                             window.EVController_01.setText('전동벨브01 ON')
                         else:
                             window.EVController_01.setText('전동벨브01 OFF')

                     if get_data[2] == '1':
                         
                        if get_data[3] =='0':
                             window.EVController_02.setText('전동벨브02 ON')
                        else:
                             window.EVController_02.setText('전동벨브02 OFF')



                     if get_data[2] == '2':
                        if get_data[3] =='0':
                             window.EVController_03.setText('전동벨브03 ON')
                        else:
                             window.EVController_03setText('전동벨브03 OFF')



                     if get_data[2] == '3':

                        if get_data[3] =='0':
                             window.EVController_04setText('전동벨브04 ON')
                        else:
                             window.EVController_04etText('전동벨브04 OFF')
            elif get_data[0] =='valvepi':
                if get_data[1] =='ar':

                        self.setWindowLabel(get_data[2])
    def setWindowLabel(self,data):
    #GUI가 실행될시에 벨브의 현재 상태를 서버에서 받을수 있다.
    #서버에서 넘어온 데이터들을 바탕으로 벨브파이의 상태를 버튼의
    #텍스트로 보여준다.
        set_data =data.split('#')
        if set_data[0] == '1' and set_data[1] =='0':
            window.EVController_01.setText('전동벨브01 OFF')
        elif set_data[0] == '1' and set_data[1] =='1':
            window.EVController_01.setText('전동벨브01 ON')


        if set_data[2] == '2' and set_data[3] =='0':
            window.EVController_02.setText('전동벨브02 OFF')
        elif set_data[2] == '2' and set_data[3] =='1':
            window.EVController_02.setText('전동벨브02 ON')
            
        if set_data[4] == '3' and set_data[5] =='0':
            window.EVController_03.setText('전동벨브03 OFF')
        elif set_data[4] == '3' and set_data[5] =='1':
            window.EVController_03.setText('전동벨브03 ON')
            
        if set_data[6] == '4' and set_data[7] =='0':
            window.EVController_04.setText('전동벨브04 OFF')
        elif set_data[6] == '4' and set_data[7] =='1':
            window.EVController_04.setText('전동벨브04 ON')
  






# 서버로 보낼때 인코딩을 알아서 해준다.
def encodeServer(strk):
    strk = str(strk)
    a = strk.encode('utf-8')
    return a


class MatplotlibWidget(QMainWindow):




    def __init__(self,displayRecv,displaySend):
        QMainWindow.__init__(self)

        loadUi("qt_designer.ui", self)            # ui파일 로드

        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")        #창 이름 설정

        

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        #숫자 버튼입력이다.
        self.num_1.clicked.connect(lambda state, button=self.num_1: self.Numclicked(state, button))
        self.num_2.clicked.connect(lambda state, button=self.num_2: self.Numclicked(state, button))
        self.num_3.clicked.connect(lambda state, button=self.num_3: self.Numclicked(state, button))
        self.num_4.clicked.connect(lambda state, button=self.num_4: self.Numclicked(state, button))
        self.num_5.clicked.connect(lambda state, button=self.num_5: self.Numclicked(state, button))
        self.num_6.clicked.connect(lambda state, button=self.num_6: self.Numclicked(state, button))
        self.num_7.clicked.connect(lambda state, button=self.num_7: self.Numclicked(state, button))
        self.num_8.clicked.connect(lambda state, button=self.num_8: self.Numclicked(state, button))
        self.num_9.clicked.connect(lambda state, button=self.num_9: self.Numclicked(state, button))
        self.num_10.clicked.connect(lambda state, button=self.num_10: self.Numclicked(state, button))


        #클라이언트 주소에 따라서 위치를 파악하기 위한 리스트들이다. 순서대로 ABCD이다.
        self.location = ['B8_27_EB_C5_1C_CA','B8_27_EB_7F_74_AA','B8_27_EB_97_BD_87','B8_27_EB_35_AB_D8']
        self.area =['A','B','C','D']

        self.reset_push.clicked.connect(self.Makereset) #숫자 초기화
        self.ent_push.clicked.connect(self.Makeent) #숫자를 토양습도로 설정
        self.ki_btn.clicked.connect(self.kisang) #기상청 정보 띄움
        self.switch_btn.clicked.connect(self.swith) #그래프 클리어

        # 통신을 위한 쓰레드
        self.displayRecv = displayRecv
        self.displaySend = displaySend

        #그래프관련 버튼
        self.graph_btn.clicked.connect(self.make_graph)

        self.back_btn.clicked.connect(self.setBeforeFile)
        self.next_btn.clicked.connect(self.setNextFile)

        #기상청에서 받은 e데이터
        self.weahter_information =  self.displayRecv.getWeahterInformation()
        self.weatherHumidity= self.weahter_information[2]
        self.weahterTeperature =self.weahter_information[1]
        self.weatherPOP = self.weahter_information[0]



        #파일을 찾기위한 수단
        self.count = 0
        self.File = self.fileFind(kind='next')


        #전동벨브 컨트롤을 할수 있는 버튼
        self.EVController_01.clicked.connect(self.sendValve1Command)
        self.EVController_02.clicked.connect(self.sendValve2Command)
        self.EVController_03.clicked.connect(self.sendValve3Command)
        self.EVController_04.clicked.connect(self.sendValve4Command)


        #시간 축 설정
        self.timeDelta = 30


        self.image_make = False
        self.manual = False
        self,displaySend.sendAR()

    def setKisang(self,humidity,temperatrue,pop): #기상청에서 받은 데이터를 사용해서 만들어준다.

        self.weatherHumidity = humidity #습도
        self.weatherTemperature = temperatrue #온도
        self.weatherPOP = pop #강수확률

    def kisang(self):
        # a = 10
        #         # b = 20
        #         # c = 30

       # msg = "현재 습도는 :%.2f%%, 현재 온도는 %s도, 현재 조도는 :%.2f%%" %(a,b,c) #원래꺼
        #서버에 기상정보를 요청을 한다
        #업데이트
        self.displaySend.sendCommand('displaypi/weatherRequest')
        msg = "현재 습도:{}  현재 온도:{}  강수확률:{} ".format(self.weatherHumidity,self.weahterTeperature,self.weatherPOP)


        QMessageBox.about(self, "기상청 정보", msg)




    def sendValve1Command(self):
        #벨브 1번관련 버튼에서 이벤트 발생시 처리하는 함수
       if self.displayRecv.manual:
            if self.EVController_01.text() == '전동벨브01 ON':
                self.displaySend.sendCommand('displaypi/command/valve01/on')
                self.EVController_01.setText('전동벨브01 WATING')
            else:
                self.displaySend.sendCommand('displaypi/command/valve01/off')
                self.EVController_01.setText('전동벨브01 WATING')
       

    def sendValve2Command(self, str):
        # 벨브 2번관련 버튼에서 이벤트 발생시 처리하는 함수
       if self.displayRecv.manual:
            if self.EVController_02.text() == '전동벨브02 ON':
                self.displaySend.sendCommand('displaypi/command/valve02/on')
                self.EVController_02.setText('전동벨브02 WATING')
            else:
                self.displaySend.sendCommand('displaypi/command/valve02/off')
                self.EVController_02.setText('전동벨브02 WATING')
       
    def sendValve3Command(self, str):
        # 벨브 3번관련 버튼에서 이벤트 발생시 처리하는 함수
        if self.displayRecv.manual:
            if self.EVController_03.text() == '전동벨브03 ON':
                self.displaySend.sendCommand('displaypi/command/valve03/on')
                self.EVController_03.setText('전동벨브03 WATING')
            else:
                self.displaySend.sendCommand('displaypi/command/valve03/off')
                self.EVController_03.setText('전동벨브03 WATING')
      

    def sendValve4Command(self, str):
        # 벨브 4번관련 버튼에서 이벤트 발생시 처리하는 함수
         if self.displayRecv.manual:
            if self.EVController_04.text() == '전동벨브04 ON':
                self.displaySend.sendCommand('displaypi/command/valve04/on')
                self.EVController_04.setText('전동벨브04 WATING')
            else:
                self.displaySend.sendCommand('displaypi/command/valve04/off')
                self.EVController_04.setText('전동벨브04 WATING')
       



    def Numclicked(self, state, button):
    #숫자 번호가 눌러졌을때 눌린 숫자를 입력창에 표시를 해준다
        exist_line_text = self.pf_line.text()

        now_num_text = button.text()

        self.pf_line.setText(str(exist_line_text + now_num_text))

        #self.pf_line.setText('{}{}'.format(exist_line_text,now_num_text))  #위에 것과 같은 버전




    def Makereset(self):
        #입력창 지우기
        self.pf_line.clear()

    def Makeent(self):
        #사용자가 토양습도를 설정했을시에 어느정도 입력을 했는지 보여준다.
        #Enter키이다.
        exist_line_text = self.pf_line.text()
        self.pf_line.clear()
        self.displaySend.sendCommand('displaypi/default/{}'.format(exist_line_text))
        QMessageBox.about(self, "message", "사용자  설정 완료:{}%".format(exist_line_text))






    def fileFind(self,kind=None):
    #그래프를 그리기위한 함수로
    #이 함수는 주소별로 나누어진 데이터를 관리하기 위해 사용된다.
    #GUI버튼에서 보면 이전센서 다음센서를 통해서 지역별 데이터를 확인이 가능하다.
    #즉 지역별 실시간 데이터를 그리기 위해 사용되는 함수이다.
        test_file = glob.glob('graphs/*.txt')
        if test_file == None:
            pass
        else:
            if kind == 'next':
                if len(test_file)-1 < self.count:
                    self.count =0
                    test_find = test_file[self.count]
                    return test_find
                else:
                    test_find = test_file[self.count]
                    self.count +=1
                    return test_find
            elif kind == 'before':
                if  self.count < 0:
                    self.count = len(test_file)-1
                    test_find = test_file[self.count]
                    return test_find
                else:
                    test_find = test_file[self.count]
                    self.count -= 1
                    return test_find


    def setNextFile(self):
    #다음센서를 눌렀을떄
        self.File =self.fileFind(kind='next')

        print(self.File)
        self.update_graph()


    def setBeforeFile(self):
    #이전센서를 눌렀을때 사용한다.
        self.File = self.fileFind(kind='before')

        print(self.File)
        self.update_graph()


    def setTimeDelta(self,timeDelta):

        self.timeDelta = timeDelta


    def make_graph(self):
    #그래프를 그려준다.
        self.image_make = True
        self.update_graph()


    def update_graph(self):
        #그래프를 그려주는 함수이다.
        #실시간 그래프를 그려줄떄는 데이터를 새로 갱신하면 실시간 그래프가 그려진다.

        # 한개의 figure객체에서 (2,2)즉 4개의 그래프창을 만든게 아니라
        # 독자적인 그래프 창을 사용한다.

        # fs = 500
        # f = random.randint(1, 100)
        # ts = 1 / fs
        # length_of_signal = 10
        # t = np.linspace(0, 1, length_of_signal)
        #
        # cosinus_signal = np.cos(2 * np.pi * f * t)

        # 실시간 그래프를 그리기 위한 가장 중요한 함수.



        #recvSock과 그래프의 동기화를 시켜야한다.
        #즉 데이터가 갱신되거나 변경이 되었을때 작동을 해야한다.
        #self.setWindowTitle(str(self.File))


        try:
            area_title =''
            #그래프를 그려지는 버튼이 안눌러졌을 시에는
            #작동이 안된다.
            if self.image_make:
                QApplication.processEvents()
                #이 함수는 중요한 이유가 GUI에 새로 갱신될때
                #알려줘야한다. 만약 저함수를 요청을 안할시에는
                #갱신이 안된다.

                title=str(self.File.replace('.txt','').replace('graphs/',''))
                #이 실시간그랲의 지역을 보여준다.

                for i,location in enumerate(self.location):
                    if location == title:
                        area_title = self.area[i]
                        print(area_title)


                self.setWindowTitle(str(area_title))
                #그지역의 위치를 제목을 보여준다.

                #한번씩 지워준다.
                self.MplWidget.canvas.axes.clear()
                self.MplWidget_2.canvas.axes.clear()
                self.MplWidget_4.canvas.axes.clear()
                self.MplWidget_3.canvas.axes.clear()


                #실시간 그래프를 그리기 위한 파일을 연다.
                sensorDatabase = open(self.File, 'r', encoding='utf-8').read()
                print('sensor')
                lines = sensorDatabase.split('\n')
                print('sensor')
                Time = []  # 시간
                humidity = []  # 습도
                solid_humidity = []  # 토양습도
                temperature = []  # 온도
                lux = []  # 조도

                for line in lines:
                    if len(line) > 1:
                        t, humidity_data, temperature_data, solid_humidity_data,lux_data,_= line.split(',')
                        Time.append(t) #시간
                        humidity.append(int(humidity_data))  # 습도
                        solid_humidity.append(int(solid_humidity_data))  # 토양습도
                        temperature.append(int(temperature_data))  # 온도
                        lux.append(int(lux_data))  # 조도
                Time = pd.to_datetime(Time)
                print('sensor')







                #humidity,temperature,solidHumidty,light
                                   # 그래프 설정
                self.MplWidget.canvas.axes.plot(Time, humidity, '--ob')
                #self.MplWidget.canvas.axes.legend('Moisture', loc='upper right')
                self.MplWidget.canvas.axes.set_title('Humidity')
                self.MplWidget.canvas.axes.xaxis_date()
                #시계열관련되서 x축을 지정해준다.
                #self.MplWidget.canvas.axes.set_xticklabels(Time, rotation=45, rotation_mode="anchor")
                self.MplWidget.canvas.axes.set_xlim(Time[-1]-timedelta(seconds=60),Time[-1])
                # 실시간 60초 기준으로 축이 변환된다.

                self.MplWidget.canvas.draw()





                 # 그래프 설정
                self.MplWidget_2.canvas.axes.plot(Time, solid_humidity, '--or')
                self.MplWidget_2.canvas.axes.set_xlim(Time[-1] - timedelta(seconds=60), Time[-1] )
                # 실시간 60초 기준으로 축이 변환된다.
                #self.MplWidget_2.canvas.axes.legend('SolidHumidity', loc='upper right')
                self.MplWidget_2.canvas.axes.xaxis_date()
                # 시계열관련되서 x축을 지정해준다.
                
                self.MplWidget_2.canvas.axes.set_title('SolidHumidity')
                self.MplWidget_2.canvas.draw()

                 # 그래프 설정
                self.MplWidget_3.canvas.axes.plot(Time, temperature, '--oy')
                self.MplWidget_3.canvas.axes.set_xlim(Time[-1] - timedelta(seconds=60), Time[-1] )
                # 실시간 60초 기준으로 축이 변환된다.
                #self.MplWidget_3.canvas.axes.legend('Tmperature', loc='upper right')
                self.MplWidget_3.canvas.axes.xaxis_date()
                # 시계열관련되서 x축을 지정해준다.
                self.MplWidget_3.canvas.axes.set_title('Teperature')
                self.MplWidget_3.canvas.draw()

                # 그래프 설정
                self.MplWidget_4.canvas.axes.plot(Time, lux, '--og')
                self.MplWidget_4.canvas.axes.set_xlim(Time[-1] - timedelta(seconds=60), Time[-1])
                #실시간 60초 기준으로 축이 변환된다.
                #self.MplWidget_4.canvas.axes.legend('LUX', loc='upper right')
                self.MplWidget_4.canvas.axes.xaxis_date()
                # 시계열관련되서 x축을 지정해준다.
                self.MplWidget_4.canvas.axes.set_title('LUX')
                self.MplWidget_4.canvas.draw()



                print('testing')
        except Exception as e:
            print(e)







        # #작동을 안함
        # def live_graph(self):
        #     QApplication.processEvents()
        #
        #     ani_0 = animation.FuncAnimation(self.MplWidget.canvas.figure,self.update_graph,interval= 1000)
        #     print('ani_01')
        #     ani_1 = animation.FuncAnimation(self.MplWidget_2.canvas.figure,self.update_graph,interval=1000)
        #     print('ani_02')
        #     ani_2 = animation.FuncAnimation(self.MplWidget_3.canvas.figure,self.update_graph,interval=1000)
        #     print('ani_03')
        #     ani_3 = animation.FuncAnimation(self.MplWidget_4.canvas.figure,self.update_graph,interval= 1000)
        #     print('ani_04')
        #
        #



    def clear(self):
    #그래프를 클리어해준다.
        self.image_make = False
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.draw()
        self.MplWidget_2.canvas.axes.clear()
        self.MplWidget_2.canvas.draw()
        self.MplWidget_3.canvas.axes.clear()
        self.MplWidget_3.canvas.draw()
        self.MplWidget_4.canvas.axes.clear()
        self.MplWidget_4.canvas.draw()

    

    def swith(self):
    #수동과 자동을 변환할때 사용되는 함수
    #이함숭서 버튼을 누르면 명령어가 서버로 통신이 된다.
        try:
            if self.switch_btn.text() == 'Auto':

                self.displaySend.sendCommand('displaypi/custum/manual')
                self.switch_btn.setText('Wating')
            elif self.switch_btn.text() =='Manual':
                self.displaySend.sendCommand('displaypi/custum/auto')
                self.switch_btn.setText('Wating')
        except Exception as e:
            print(e)


    #
    # def updateGraph(self):
    #




if __name__ == "__main__":
    host = 'B8:27:EB:D0:AA:C5'
    # 포트주소 블루투스는 0~100번대의 포트가 존재한다.
    port = 2
    # host = 'localhost'
    # port = 1803
    while True:
        try:
            # 블루투스를 RFCOMM방식으로 요청한다.
            sock = BluetoothSocket(RFCOMM)
            # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            # 동기화를 위한 Thread의 락이다
            # 락을 얻은 쓰레드는 우선권을 얻어
            # 다른 쓰레드들이 기다리고 락을 얻은
            # 쓰레드만 사용이 가능하다.
            lock = threading.Lock()
            # 접속이 성공적으로 되면 loop에서 빠져나간다.
            break

        # 만약 접속실패시 재접속을 한다.
        except ConnectionRefusedError:
            time.sleep(2)
            pass

    lock = threading.Lock()
    displayRecv = displayRecv(sock)
    print('start')


    displaySend =displaySend(sock)
    print('start')

        
    displaySend.start()
    displayRecv.start()

    register_matplotlib_converters() #FutureWarning 방지
    app = QApplication(sys.argv)
    window = MatplotlibWidget(displayRecv=displayRecv,displaySend=displaySend)



    
    window.show()   #창 띄움

    app.exec_()





