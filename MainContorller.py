

import threading
#Thread 모듈
import queue
#데이터를 하나씩 처리하기위한 큐
import complexWeather as cw
#기상청 API를 사용하기 위해 만들어둔 커스텀 모듈
import time
#시간 지연을 위한 모듈
import os
#폴더및 파일을 생성시 사용하는 모듈
import json
#json형태의 데이터를 처리하는 데이터
from time_z import weatherTime
#기상청API에 필요한 시간형식을 위한 모듈

from datetime import datetime
#블루투스 통신을 위한 모듈
from bluetooth import *

defaul_POP = 60


class weatherCall(threading.Thread):
    #서버측에서 기상청API에 접속을 한다.

    def __init__(self):
        threading.Thread.__init__(self)
        self.count = 0 #몇번쨰 요청을 했는지 파악하기 위한 변수
        self.POP_data =50 #강수확률
        self.T3H_data = -1 #3시간최고온도
        self.REH_data = -1 #습도도



    def run(self):
        while True:
            wt = weatherTime()

            self.count += 1
            testWeather = cw.weatherUrl()
            #기상청 API를 요청하는 구문
            a = testWeather.parsedUrl(testWeather.ForestSpaceCheck)
            #테스트라는 폴더의 존재를 확인하여
            #존재하지않을시에 생성을 한다.
            if os.path.isdir('test'):
                pass

            else:
                os.makedirs('test')
            #test폴더안에 날짜 시간별로 기상청 API의 데이터를 저장한다.
            with open('test/{}.json'.format(wt.date() + wt.time()), 'w', encoding='utf-8') as make_file:
                json.dump(a, make_file, ensure_ascii=False, indent="\t")
            #강수확률 데이터 저장
            self.POP_data =int(float(self.findCategory(parsed_data=a,category='POP'))) #강수확률
            #3시간 온도 저장
            self.T3H_data = int(float(self.findCategory(parsed_data=a,category='T3H'))) #3시간 기온
            #습도 저장
            self.REH_data =int(float(self.findCategory(parsed_data=a,category='REH'))) #습도
            print(self.POP_data)
            print(self.T3H_data)
            print(self.REH_data)


            #요청이 될때 날씨 정보를 GUI에게 보내준다.
            self.sendWeahterInformation()
            print('sendWeatherInformation')






            #3시간에 한번씩 돌린다.
            time.sleep(3*60*60)

    def sendWeahterInformation(self):
    #기상정보를 보내는 함수
            sendall('server/weatherInformation/{},{},{}'.format(self.POP_data,self.T3H_data,self.REH_data))

    def findCategory(self,parsed_data = None, category=None):
    #데이터 파싱을 위한 함수
        if parsed_data ==None:
            pass
        if category ==None:
            pass

        for i in range(len(parsed_data)):

            if parsed_data[i]['category'] == category:
                return parsed_data[i]['fcstValue']



class multiThreadServer(threading.Thread):
    #메인서버로서 여러개의 클라이언트를
    #멀티쓰레드 기법을 사용해서 한다.
    weatherCall
    #쓰레드를 관리하는 리스트이다.
    global th_list
    def __init__(self,sock,address):
        threading.Thread.__init__(self)
        #클라이언트 접속시 사용되는 소켓을 생성시에 넣는다.
        #그 값을 이제 클래스 내부에서 사용한다.
        self.sock = sock
        #daemon은 MainTrhead가 종료되면 백그라운드에 있는
        #쓰레드들도 끝난다.
        self.daemon=True
        #데이터를 하나씩 처리하기 위한큐
        self.queue = queue.Queue()
        #접속된 클라이언트들의 주소
        self.address =address
        #접속 된 클라이언들의 주소를 사용하기 편하게 파싱을 한다.
        self.parsing_address = str(address).replace(':','_')
        '''
        :를 사용했지만 text파일 생성시 이름에서:앞에만 짤리는 오류를 발견 '-'로 대체함
        블루투스는 :로 주소가 나눠진다. 따라서 :를 '-'로 대체를 하여 사용을 한다.
        '''

        # self.dispaly_connection =False #디스플레이의 요청에 따라 그래프를 그려준다.
        # self.diplay_graph_list =['solidHumidity','temperature','humidity','light']
        # self.display_solidHumidry=False
        # self.dispaly_temperature=False
        # self.display_humidity = False
        # self.display_light =False
        #
        self.defaultSolidHumidity = -1 #사용자 지정 토양습도값
        self.check_solidHumidity = -1 #두개의 변수 음의 값인 이유는 자동비교를 막기 위한 수단이다.



    def run(self):

        try:

            #self.sock.send(encodeServer('hello SCW'))
            while True:

                time.sleep(0.1)
                #lock.acquire()
                data = self.sock.recv(1024).decode('utf-8')
                que_data=self.queue.put(data)
                get_data = self.queue.get().split('/')
                print(get_data)
                #문자열 통신에서 명령어는 pi종류/센서/상태/개수/데이터
                #데이터는 ,(comma)기준으로 나눠진다.

                if len(get_data) <=6:
                    if get_data[0] == 'sensorpi':

                        #초장기 토양습도센서를 받는 방법
                        if get_data[1] == 'solidhumidity':

                            if get_data[2] == '1':

                                 sensor_counts=int(get_data[3])
                                 sensor_data =get_data[4].split(',')
                                 print(sensor_data)
                            else:
                                pass





                        #초장기의 조도센서 받는 구문
                        elif get_data[1] ==  'cds':
                            print(get_data[1])

                            if get_data[2] == '1':

                                    sensor_counts = int(get_data[3])
                                    sensor_data = get_data[4].split(',')
                                    print(sensor_data)
                            else:
                                pass
                        #초장기 온도를 받는 구분
                        elif get_data[1] == 'temperature':
                            print(get_data[1])
                            if get_data[2] == '1':

                                sensor_counts = int(get_data[3])
                                sensor_data = get_data[4].split(',')
                            else:
                                pass

                        #초장기 습도를 받는 구문
                        elif get_data[1] == 'humidity':

                            print(get_data[1])

                            if get_data[2] == '1':

                                sensor_counts = int(get_data[3])
                                sensor_data = get_data[4].split(',')
                        #센서파이에서 넘어오는 값들을 처리하는 메인서버 구문이다.
                        elif get_data[1] =='sensordata':
                            print('databaseworking')
                            sensor_check = get_data[2].split('%') #데이터는 시간,습도, 토양습도, 온도,조도, 강수확률순으로 저장한다.
                            #자동비교를 위해 변수에 넘어온 토양습도 값을 저장한다.
                            self.check_solidHumidity = int(sensor_check[1])
                            print(self.check_solidHumidity)
                            print('BeforeCompare')
                            #위에 self.check_solidHumidity의 값으로 비교를 한다.
                            self.compareValve()
                            print("AfrterCompare")
                            #넘어온 값들을 문자열 파싱을 하여 GUI에게 보낸다.
                            sensor_check = str(sensor_check).replace('[','')
                            sensor_check = str(sensor_check).replace(']','')
                            sensor_check = sensor_check+','+str(self.parsing_address)

                            print(sensor_check)
                            send_sensordata = "server/display/{}%{}".format(get_data[2],self.parsing_address)
                            # time.sleep(5) #테스트용


                            print(send_sensordata)
                            #파싱된 센서들의 값을 저장하는 구문이다.
                            sensor_check = sensor_check+'\n'
                            #이 데이터들을 전 클라이언트들에게 보낸다.
                            sendall(send_sensordata)
                            with open('sensorDatabase.txt','a+t',encoding='utf-8') as sd:
                                sd.writable()
                                sd.write(sensor_check)






                        else:
                            pass



                    #'valvepi/valvenumber/1/0'
                    #벨브파이의 상태를 받아 전달하는 명령어이다.
                    elif get_data[0] == 'valvepi':


                            if get_data[1] == 'valvenumber':


                                if get_data[2] == '1':
                                    if get_data[3] == '0':
                                        sendall('server/valvestate/1/0')

                                    else:
                                        sendall('server/valvestate/1/1')

                                elif get_data[2] == '2':

                                    if get_data[3] == '0':

                                        sendall('server/valvestate/2/0')

                                    else:

                                        sendall('server/valvestate/2/1')


                                elif get_data[2] == '3':

                                    if get_data[3] == '0':

                                        sendall('server/valvestate/3/0')

                                    else:

                                        sendall('server/valvestate/3/1')


                                elif get_data[2] == '4':

                                    if get_data[3] == '0':

                                        sendall('server/valvestate/4/0')

                                    else:

                                        sendall('server/valvestate/4/1')

                            #벨브의 자동및 수동 모드의 상태를 알려주는 문자열이다.
                            elif get_data[1] =='valvecustum':
                                if get_data[2] =='auto':
                                    sendall('server/valvecustum/auto')
                                elif get_data[2] =='manual':
                                    sendall('server/valvecustum/manual')
                            #GUI 클라이언트에 벨브파이의 상태를 전송하는 구문이다.
                            elif get_data[1] =='displaypi':
                                if get_data[2] =='ar':
                                    sendall('valvepi/ar/{}'.format(get_data[3]))





                    elif get_data[0] == 'displaypi':
                    #GUI에서 기상청 정보를 요청할떄 사용되는 데이터이다.
                        if get_data[1] == 'weatherRequest':
                            weatherCall.sendWeahterInformation()

                    #GUI에서 사용자가 토양습도 설정시 이 데이터들을 보내준다.
                        elif get_data[1] == 'default':
                            self.defaultSolidHumidity=int(get_data[2])
                            for i in th_list:
                                i.defaultSolidHumidity=int(get_data[2])

                        #'displaypi/command/valve04/on'
                        #GUI에서 벨브를 키고 끌때 사용되는 명령어이다.
                        elif get_data[1] == 'command':
                            if get_data[2] =='valve01':
                                if get_data[3] == 'on':
                                    sendall('server/valvepi/valve01/on')

                                else:
                                    sendall('server/valvepi/valve01/off')
                            elif get_data[2] == 'valve02':

                                if get_data[3] == 'on':
                                    sendall('server/valvepi/valve02/on')

                                else:
                                    sendall('server/valvepi/valve02/off')

                            elif get_data[2] == 'valve03':

                                if get_data[3] == 'on':
                                    sendall('server/valvepi/valve03/on')

                                else:
                                    sendall('server/valvepi/valve03/off')

                            elif get_data[2] == 'valve04':

                                if get_data[3] == 'on':
                                    sendall('server/valvepi/valve04/on')

                                else:
                                    sendall('server/valvepi/valve04/off')
                        elif get_data[1] == 'custum':
                            if get_data[2] =='manual':
                                sendall('server/custum/manual')
                            elif get_data[2] == 'auto':
                                sendall('server/custum/auto')

                        elif get_data[1] == 'valvepi':
                            #G
                            if get_data[2] =='allrequest':
                                sendall('server/valvepi2/allrequest')


                        #초장기 각각의 데이터의 요청에 따라 GUI에 그려주는 것을 구상을 했지만 값들을 다 보여주는게
                        #사용자한테 편리하다는 것을 판단을 함
                        # if get_data[1] == '1':
                        #   for i in self.diplay_graph_list: #self.diplay_graph_list =['solidHumidity','temperature','humidity','light']
                        #     if get_data[2] == str(i):
                        #         str(i)
                        #         if i == self.diplay_graph_list[0]:
                        #             self.display_solidHumidry=True
                        #         elif i == self.diplay_graph_list[1]:
                        #             self.diaply_temperature=True
                        #         elif i == self.diplay_graph_list[2]:
                        #             self.display_humidity=True
                        #         elif i == self.diplay_graph_list[3]:
                        #             self.display_light=True
                        #         else:
                        #             pass
                        # elif get_data[1] == '0':
                        #     for i in self.diplay_graph_list:  # self.diplay_graph_list =['solidHumidity','temperature','humidity','light']
                        #         if get_data[2] == str(i):
                        #             str(i)
                        #             if i == self.diplay_graph_list[0]:
                        #                 self.display_solidHumidry = False
                        #             elif i == self.diplay_graph_list[1]:
                        #                 self.dispay_temperature = False
                        #             elif i == self.diplay_graph_list[2]:
                        #                 self.display_humidity = False
                        #             elif i == self.diplay_graph_list[3]:
                        #                 self.display_light = False
                        #             else:
                        #                 pass
                        #

                        # 그래프를 그릴때 address(즉 블루투스당 그래프를 그려야할지 고민을 해봐야겠다.)

                        # elif self.display_solidHumidry:
                        #     self.sock.send()
                        #
                        # elif self.display_humidity:
                        #     self.sock.send()
                        # elif self.diaply_temperature:
                        #     self.sock.send()
                        #
                        # elif self.display_light:
                        #     self.sock.send()

                else:
                    pass














        except IOError:
        #만약 접속 에러가 발생했을때 그 thread를 관리하는 리스트에서
        #삭제를 한다.
            for i in th_list:

                if i.name == self.name:
                    th_list.remove(i)

                    print('{} exit'.format(self.name))

            print('remove')

            self.sock.close()


        except ConnectionResetError:
            # 만약 접속 에러가 발생했을때 그 thread를 관리하는 리스트에서
            # 삭제를 한다.
            for i in th_list:

                if i.name == self.name:
                    th_list.remove(i)

                    print('{} exit'.format(self.name))

            print('remove')

            self.sock.close()


    #센서파이 전부다 습도 비교
    #센서파이와 기상처 api습도,강수량,강수확률 비교
    #인공지능 모델과 비교
    #조도센서 받기
    #온도센서 받기
    #토양습도센서
    #디스플레이 센서에서 받은 값을 서버한테 넘겨주는 명령어를 만들어야한다.
    #

    def compareValve(self):
    #사용자 토양습도값과 센서파이들의 토양습도값들을 비교한다.

        print(self.check_solidHumidity > 0 and self.defaultSolidHumidity >0)
        print(self.check_solidHumidity)
        print(self.defaultSolidHumidity)
        if self.check_solidHumidity > 0 and self.defaultSolidHumidity >0 :

            compare_value = self.defaultSolidHumidity -self.check_solidHumidity
            #만약 물을 줘야한다면 밑에 조건문이 작동
            if compare_value >=0:
                print('compareon')
                sendall('server/valveCompare/{}/{}'.format(self.address,compare_value))
            #물을 안줘도 될때 아래 조건문이 작동
            elif compare_value <0:
                print('compareoff')
                sendall('server/valveStop/{}'.format(self.address))

def encodeServer(strk):
    #encdoing하는 함수
    strk = str(strk)
    a = strk.encode('utf-8')
    return a


def sendall(str):
    #모든 클라이언들에게 정보 전송
    #보내는 와중에 문자열들이 끼어들면 안되기 떄문에
    #LOCk을사용해 동기화를 시킨다.
    lock.acquire()
    try:

        for i in th_list:


            i.sock.send(encodeServer(str))

    except Exception:
        pass
    lock.release()

# def commandinput(inputs, command_list):
#
#
#
#             while True:
#                 input_str = input(inputs).strip()
#
#                 for i in command_list:
#                     print(i)
#                     if input_str == str(i):
#                         return str(i)
#                     else:
#                         print('명령어 리스트없는 값입니다.'.format(command_list))
#                         pass

port=2
#빈칸으로 호스트를 호출할시에 자기자신의 주소를 집어넣는다.
host = ''
#port = 1803
#multi_trhead를 활용하기 위한 리스트 생성
th_list = []
#기상청 API에서 데이터를 받기위한 thread 생성
weatherCall=weatherCall()
#기상청 APIthread 시작
weatherCall.start()
sock=BluetoothSocket(RFCOMM)
#sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(2)
#데이터를 보내는 과정의 큐를 사용함
sending_que = queue.Queue()
while True:
    #비동기화 통신에서 동기화가 필요할때 사용하는 값
    lock = threading.Lock()
    #클라이언트가 서버에 접속을 했을시에
    #클라이언트 이름과 주소를 반환하는 함수이다.
    #accept함수는 클라이언트가 접속을 할때까지 기다린다.
    client, address = sock.accept()
    print('주소가 {}인 클라이언트({})의 접속했습니다'.format(address,client))
    #접속시 그 클라이언트을 넣은 Thread를 생성한다.
    clientThread=multiThreadServer(client,address[0])
    #Thread관리를 위한 리스트에 집어넣는다.
    th_list.append(clientThread)
    print(clientThread)
    #Thread시작.
    clientThread.start()

    #새로운 클라이언트 접속시 날씨 데이터를 전송해준다.
    print('reSendingWeather')
    #접속시 날씨 데이터를 업데이트를 해준다.
    weatherCall.sendWeahterInformation()



