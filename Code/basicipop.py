# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:07:19 2022

@author: techv
"""
import serial
import time

ser = serial.Serial('COM9',baudrate=9600,timeout=0.5)

I = 750
J = 0

while True:
    ser_bytes = ser.readline().decode("utf-8").rstrip()
    
    data = ser_bytes.split("\r")
    # print(data)
    if data[0] != "": 
        print(data[0])
        I=750
        J=750
        ser.write(b"hii man rpii")
        print(data[0])
        
    time.sleep(0.1)
        