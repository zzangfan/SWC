# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 21:51:02 2019

@author: defautl
"""

#풍향값에 따른 16 방위 변환식

#(풍향값+22.5*0.5/22.5) = 변환값(소수점 이하 버림)
import re

"""
기상청 api로 부터 받은 데이터를
json파싱을 통해서 받은 파일을
범주형 값들을 변환한다.
"""
test =['강수확률은 10(%) 입니다',
       '강수형태은 0 입니다', 
       '6시간 강수량은 0(mm) 입니다', 
       '습도은 75(%) 입니다', 
       '6시간 신적설은 0(cm) 입니다', 
       '하늘상태은 2 입니다', 
       '풍속[동서성분]은 1.7(m/s) 입니다', 
       '풍향은 330(m/s) 입니다', 
       '풍속[남북성분]은 -2.9(m/s) 입니다']



class categoryParsing:
    
    
    def __init__(self):
        self.wind16 = {0:'N',
                  1:'NNE',
                  2:'NE',
                  3:'ENE',
                  4:'E',
                  5:'ESE',
                  6:'SE',
                  7:'SSE',
                  8:'S',
                  9:'SSW',
                  10:'SW',
                  11:'WSW',
                  12:'W',
                  13:'WNW',
                  14:'NW',
                  15:'NNW',
                  16:'N'}
        #적설 범주 및 표시방법(값) 카테고리
        self.S06_Category={0:'0cm',
              1:'1cm 미만',
              5:'1~4cm',
              10:'5~9cm',
              20:'10~19cm',
              100:'20cm 이상'}
        #강수량 문자열 표시 카테고리                   
        self.R06_Category={0:'0mm',
              1:'1mm미만',
              5:'1~4mm',
              10:'5~9mm',
              20:'10~19mm',
              40:'20~39mm',
              70:'40~69mn',
              100:'70mm 이상'
        }
        
        
    
    #풍향값에 따른 16방위 변환식
    def getWeather16(self,x):
        
        
        
            
        return int((x+22.5*0.5)/22.5)
    
    
    
    def getWindSpeed(self,x,type=None):
        windStrenght =['바람이 약한','바람이 약간 강한','바람이 강한','바람이 매우 강한']
        
        if type=='UUU':
            if x>=0:
            
                if x<4: 
                    
                    return "풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('동쪽',x,windStrenght[0])
                if x<9 and x>=4:
                    return "풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('동쪽',x,windStrenght[1])
                    
                if x<14 and x>=9: 
                    return "풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('동쪽',x,windStrenght[2])
                    
                if x>=14: 
                    return "풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('동쪽',x,windStrenght[3])
                    
            else:
                
                x=abs(x)
                
                if x<4: 
                    return "풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('서쪽',x,windStrenght[0])
                    
                if x<9 and x>=4:
                    return"풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('서쪽',x,windStrenght[1])
                    
                if x<14 and x>=9: 
                    return "풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('서쪽',x,windStrenght[2])
                    
                if x>=14: 
                    return "풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('서쪽',x,windStrenght[3])
                    
                
        if type=='VVV':
            if x>=0:
                
                if x<4: 
                    return"풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('북쪽',x,windStrenght[0])
                    
                if x<9 and x>=4:
                    return "풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('북쪽',x,windStrenght[1])
                    
                if x<14 and x>=9: 
                    return "풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('북쪽',x,windStrenght[2])
                    
                if x>=14: 
                    return"풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('북쪽',x,windStrenght[3])
                    
            else:
                    
                x=abs(x)
                    
                if x<4: 
                    return"풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('남쪽',x,windStrenght[0])
                    
                if x<9 and x>=4:
                    return"풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('남쪽',x,windStrenght[1])
                    
                if x<14 and x>=9: 
                    return"풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('남쪽',x,windStrenght[2])
                    
                if x>=14: 
                    return"풍속은 {}으로 {}(m/s)이고 바람이 {}편입니다.".format('남쪽',x,windStrenght[3])
                    
        
    """def getSkySpeed(skycondition=None):
        if skycondition ==None:
            print('값을 입력하세요')
        if skycondition >=0  and skycondition <=2:
            return '맑음'
        if skycondition >=3  and skycondition <=5:
            return '구름조금'
        if skycondition >=6  and skycondition <=8:
            return '구름 많음'
        if skycondition >=9  and skycondition <=10:
            return '흐림'
    """
    #SKY상태
    def getSkycondition(self,x):
        if x==1:
            return '맑음'
        if x==2:
            return '구름조금'
        if x==3:
            return '구름 많음'
        if x==4:
            return '흐림'
        
    def getRS(self,x,type=None):
        if type =='rain':
            if x in self.R06_Category:
                
                return self.R06_Category.get(x)
        if type =='snow':
            if x in self.S06_Category:
                
            
            
                return self.S06_Category.get(x)
            
        
        