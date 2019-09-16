# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 08:58:48 2019

@author: zzangfan
"""
import urllib.request as rs
#인터넷의 url을 불러오는 모듈
import json
#json형태의 파일을 읽고 처리하기 위한 모듈
import xml
#xml형태의 파일을 읽고 처리하기 위한 모듈

from time_z import weatherTime
#기상청 API시간에 필요한 함수들을 모은 모듈
from key import key
#기상청 API에 접근할때 사용자에게 할당된 키
import datetime
#날짜와 시간이 관련된 모듈
from datetime import timedelta
#시간을 비교하기 위한 모듈
import pytz
#시간 관련 모듈 한국기준 시간으로 잡아주느 모듈
from weater16 import categoryParsing as cp #파싱을 위한 카테고리 보관소


z_key = key()


#초단기 버전
class key:
    def __init__(self):
        self.key=str(z_key.key)
    def input(self,key):
        self.key =key
        return
        
        
class weatherUrl:
    '''
    기상청 API는 URL형태로 요청을 하면
    기상청에서 요청 상황과 맞게 기상 예보를 보내준다.
    따라서 URL형태로 만들때의 지정된 형태가 있어 그 형태를 맞춰줘야한다
    기상청 API의 카테고리의 맞게 파싱을 해줘야하기 때문에 사용하는 클래스이다.

    '''
    
    weaterkey = key()
    def __init__(self):
        self.cp =cp()
        self.today = weatherTime()#오늘 날짜를 보기위해 객체선언
        self.serviceKey= self.weaterkey.key#사용자 키
        self.base_date  = self.today.date() #요청시의 날짜
        self.base_time  = self.timeCheck(time_table=self.get_standard_time())#요청시의 시간
        self.nx ='63'#전북대학교 기준좌표 x:63 y:89
        self.ny ='89'
        self.numOfRows='10' #요청시 열의 수
        self.pageNo='1'
        self._type='json' #요청시의 데이터의 형태
        #동네예보 카테고리
        self.forestspace_category = {
                    'POP':['강수확률','(%)'],
                    'PTY':['강수',"형태"],
                    'R06':['6시간 강수량','(mm)'],
                    'REH':['습도','(%)'],
                    'S06':['6시간 신적설','(cm)'],
                    'SKY':['하늘',"상태"],
                    'T3H':['3시간 기온','°C'],
                    'TMN':['아침 최저 기온','°C'],
                    'TMX':['낮 최고 기온','°C'],
                    'UUU':['풍속[동서성분]','(m/s)'],
                    'VVV':['풍속[남북성분]','(m/s)'],
                    'WAV':['파고','(M)'],
                    'VEC':['풍향','(m/s)'],
                    'WSD':['풍속','(m/s)']}
        #초단기실황 예보 카테고리
        self.forestData_category = {
                'T1H':['기온','°C'],
                'RN1':['1시간 강수량','mm'],
                'UUU':['동서바람성분','m/s'],
                'VVV':['남북바람성분','m/s'],
                'REH':['습도','%'],
                'PTY':['강수형태','코드값'],
                'VEC':['풍향','0'],
                'WSD':['풍속','1']
                }
        #초단기예보
        self.forestGrib_category = {
                'T1H':['기온','°C'],
                'RN1':['1시간 강수량','mm'],
                'SKY':['하늘상태','코드값'],
                'UUU':['동서바람성분','m/s'],
                'VVV':['남북바람성분','m/s'],
                'REH':['습도','%'],
                'PTY':['강수형태','코드값'],
                'LGT':['낙뢰','코드값'],
                'VEC':['풍향','0'],
                'WSD':['풍속','1']
                
                
                }
        
        
    def get_standard_time(self):
        #기상청 API에서는 2,5,8,11,14,17,20,23의 baseTime만을 요청해야
        #사용이 가능하다. 따라서 그 사이의 있는 시간은 저 시간안으로 바꿔저야한다.
        standard_time = [2, 5, 8, 11, 14, 17, 20, 23]
        return standard_time
        

        
    #url생성시 사용되는 함수
    def setParameter(self,base_date=None,
               base_time=None,
               nx=None,
               ny=None,
               numOfRows = None,pageNo = None,
               _type=None):
        
        if base_date is not None:
             self.base_date=str(base_date)
        if base_time is not None:
            self.base_time =str(base_time)
        if nx is not None:
            self.nx = str(nx)
        if ny is not None:
            self.ny = str(ny)
        if numOfRows is not None:
            self.numOfRows = str(numOfRows)
        if pageNo is not None:
            self.pageNo = str(pageNo)
        if _type is not None:
            self._type =str(_type)
        
        
        
        
        
    @property    
    def get_subUrl(self):
        #기상청에서 url로 데이터를 요청할때 필요한 url
        app_servicekey='serviceKey={}'.format(self.serviceKey)
        app_base_date ='&base_date={}'.format(self.base_date)
        app_base_time ='&base_time={}'.format(self.base_time)
        app_nx ='&nx={}'.format(self.nx)
        app_ny ='&ny={}'.format(self.ny)
        app_numOfRows ='&numOfRows={}'.format(self.numOfRows)
        app_pageNo='&pageNo={}'.format(self.pageNo)
        app_type='&_type={}'.format(self._type)
        
        return app_servicekey+app_base_date+app_base_time+app_nx+app_ny+app_numOfRows+app_pageNo+app_type
        


    #동네예보 조회
    #지역한정으로 데이터를 준다.
    @property
    def  ForestSpaceCheck(self):
        url='http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData'
        com_url="{}?{}".format(url,self.get_subUrl)
        return com_url
        
      
    #초단기예보조회 
    @property    
    def ForestTimeData(self):
        url=' http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastTimeData'
        com_url="{}?{}".format(url,self.get_subUrl)
        return com_url
        
    #초단기실황조회
    @property
    def ForesecastGrib(self):
        url='http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib'
        com_url="{}?{}".format(url,self.get_subUrl)
        return com_url
    
            
    
        
    
    #Json타입 형태에 url을 열때 사용하는 함수
    
    
    def parsedUrl(self,url=None, url_type='json',type=None):
        #url을 파싱을 하는곳이다. Url데이터 형태에 따라 파싱에 사용되는 모듈이
        #차이가 있기 때문에 요청되는 데이터의 따라서 처리가된다.
    
        #Json타입:json을 입력
        #:xml을 입력
        if url == None and type ==None:
            print('url을 확인하세요')
            return
            
        if type == None:
            pass
            
        if url == None:    
            if type == 'check':
                url= self.ForestSpaceCheck
            if type =='grib':
                url= self.ForesecastGrib
            if type =='data':
                url = self.ForestTimeData

        
        #Json 
        
        if(url_type=='json'):
             #넘어오는 url의 encoding형태는 utf8 이다.
             #따라서 url의 decoding을 utf8로 안해주시에
             #문자들이 이상하게 파뀐다.
              urlopen=rs.urlopen(url).read().decode('utf8')

             #필요한 부분만 추출하는 과정이다.
              try:parsed_data=json.loads(urlopen)['response']
              except :
                      print(parsed_data)
              try:parsed_data=parsed_data['body']
                  
              except :
                  print(parsed_data)
              try:parsed_data=parsed_data['items']
            
              except :
                print(parsed_data)
                  
              try:parsed_data=parsed_data['item']
                     
              except :
                  print(parsed_data)
                  
             
              

              return parsed_data
    

    
      
        
        
        
        
        
        
    def forestPredict(self,parsed_json=None,category=None):
        #요청된 3가지 유형중 하나일때 그것에 맞는 파싱을 해주는 함수이다.
        if(parsed_json==None or category==None):
           return
        
        
        c=parsed_json
        weather_category=category
        #test라는 리스트안에 날씨의 관련된 데이터를 파싱하여 집어넣는다.
        test = []
        for z in range(len(c)):
            for i in weather_category:
                #특정값들은 수치값이 카테고리 값이기때문에 INT로 형변환시 문제가 발생하여
                #특정 category의 값들은 손수 처리를 해줬다.
                if c[z]['category'] == i:
                    
                    if c[z]['category'] == 'SKY':
                        
                        test.append(self.cp.getSkycondition(c[z]['fcstValue']))
                       
                    if c[z]['category'] == 'UUU':
                        test.append(self.cp.getWindSpeed(c[z]['fcstValue'],type='UUU'))
                    
                    
                    if c[z]['category'] == 'VVV':
                         test.append(self.cp.getWindSpeed(c[z]['fcstValue'],type='VVV'))
                        
                    if c[z]['category'] == 'WAV':
                        test.append(self.cp.getWeather16(c[z]['fcstValue']))
                         
                    else:
                        if len(weather_category.get(i))<2:
                            test.append(weather_category.get(i)[0]+'은 '+str(c[z]['fcstValue'])+' 입니다')
                                   
                        else:
                            test.append(weather_category.get(i)[0]+'은 '+str(c[z]['fcstValue'])+weather_category.get(i)[1]+' 입니다') 
        return test
        
    #요청한 시간을 기상청 API요청시 사용되는 시간에 맞게 해주는 함수이다.
    def timeCheck(self,time_table=None):
    
        a=datetime.datetime.now()
        
        for i in range(len(time_table)):
    
            if(i+1<len(time_table)):
                #기상청 API에서 데이터를 제공하는 시간은 baseTime 0200일때는  2시 10분이 넘어야 그때 정보가 갱신된다.
                #만약 데이터가 없는데 요청을 하는 경우에는 기상청 API에서 오류값들이 넘어온다.
                if a>datetime.datetime(a.year,a.month,a.day,time_table[i],10) and a<datetime.datetime(a.year,a.month,a.day,time_table[i+1],10):
                    #baseTime같은 경우 2시는 0200식의 문자열클래스로 반환이 되어야 한다.
                    #따라서 zfill 문자열의 내장함수를 사용해서 처리를 한다.
                    return str(time_table[i]).zfill(2)+'00'

            else:
                #기상청 API에서 가장 시간이 많이들어간 구문이다.
                #기상청 API에서 다음날 새벽 0100시에 요청을 해야할때는 baseDate가 그전날이여야한다.
                #현재 시간으로 요청할시에는 그 다음날에 다음날이 요청이 되기 때문에 기상청 API에서는 아직 예보가 안된
                #baseDate이기 때문에 오류가 발생한다. 따라서 이 것을 처리하기 위해서 다음 조건문을 만들었따.

                #23시 10분에서 자정까지는 위에 문제가 발생을 안한다.
                if a>datetime.datetime(a.year,a.month,a.day,23,10) and a<datetime.datetime(a.year,a.month,a.day,23,10)+timedelta(hours=1,minutes=30): 
                    return '2300'
                #만약 새벽 0시에서 2시10분정에 시간에 요청을 할때는 그 전날 baseDate로 조정을 해야한다.

                if (a>=datetime.datetime(a.year,a.month,a.day,0,0) and a<datetime.datetime(a.year,a.month,a.day,2,10)):
                    #base_date를 전날로 바꿔주는 객체를 선언한다.
                    self.base_date=self.today.beforetime()
                    return '2300'
    
    

    
    def getSiganlCategry(self,i): 
        if i in self.forestspace_category:
            a=self.forestspace_category.get(i)
        
        return a
    

    def predictTest(self,a):
    #사용자가 쉽게 정보를 파악할수 있게 파싱을 해주는 함수
        data= []
        for i in a:
            
            c= '기준시간은 {}:{}이고 예측시간은{}:{}에 {}은 {}{}입니다.'.format(i['baseDate'],
                      i['baseTime'],
                      i['fcstDate'],
                      i['fcstTime'],
                      self.getSiganlCategry(i['category'])[0],i['fcstValue'],self.getSiganlCategry(i['category'])[1])
            
            data.append(c)
        return data
            
    @property
    def getTime(self): #현재 요청한 기상청 API의 요청한 base날짜와 시간을 얻기 위한 함수
        
        return "{} {}".format(self.base_date,self.base_time)


    def setData(self,parsed_data=None):  #기상청 api에서 받은 데이터를 습도값과 비교하기 위해 저장을 한다.

        c ={}
        for n,i in enumerate(parsed_data):
            if parsed_data[n]['category']=='POP': #강수확률
                c['POP']=parsed_data[n]['fcstValue']
            elif parsed_data[n]['category']=='R06': #6시간 강수량
                c['RO6']=parsed_data[n]['fcstValue']
            elif parsed_data[n]['category']=='REH': #습도
                c['REH']=parsed_data[n]['fcstValue']
        
        return c
    
        
        
    
    