# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 10:45:01 2019

@author: zzangfan
"""
from datetime import datetime,timedelta



class weatherTime:
    now = datetime.now()
    def __init__(self):
        self.now =datetime.now()
        
    #현재 날짜를 스트링값으로 반환한다.
    def date(self):
        return str(self.now.strftime('%Y%m%d'))
    
    def time(self):#시간
        return str(self.now.strftime('%H%M%S'))
    #새벽 1시 에는 전날 기준으로 데이터를 보내줘야 현재의 시간의 날씨를 예보해준다.
    #따라서 그에 따른 함수이다.
    def beforetime(self):
        c= datetime(self.now.year,self.now.month,self.now.day)-timedelta(days=1)
        return str(c.strftime('%Y%m%d'))
        
    
    
    
    
    

        


   
        
        
        
