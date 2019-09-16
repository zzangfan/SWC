# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 13:35:44 2019

@author: defautl
"""
from datetime import datetime

class key:
    def __init__(self):
        self.key = 'ny1LVvumH20TW%2Fjytb5ek%2Br6i7Xs2pxQ9XoIuNtIlPNfBreOkobUkxgs7UOxgT3wEfPfAd7AWApqYW5P3JYLFA%3D%3D'
        

class time:
    def __init__(self):
        
        self.now = datetime.now()
       
        
    def baseDate(self): #현재 시간 YYYYMMDD로 나타낸다.
        
        return str(self.now.year) +str(self.now.month).zfill(2)+str(self.now.day)
    
    
    def baseTime(self): #현재 시간을 나타낸다
        return str(datetime.now().hour).zfill(2)
        
        
        
      

        
    
         
    
        
            
    
        