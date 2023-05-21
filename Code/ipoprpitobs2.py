import serial
import time
from numpy import *
from tkinter import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
import random

current_pose = [0,0,0]
prev_x,prev_y,prev_w1,prev_w2 = 0,0,0,0

lmotor_max = 1500
rmotor_max = 0

lmotor_min = 750
rmotor_min = 750
rotate = 1

def __init__():
    ser = serial.Serial('/dev/ttyS0',baudrate=9600,timeout=0.05)
    return ser
  
def get_position(x,y,c1,c2,current_pose,rotate,t):
    d1 = float(c1) * 8.125
    d2 = float(c2) * 8.125
    print(t)
    d_dist = d1
    if rotate == 1 or rotate == -1:
        #d_theta = 360*c2*32.5*t/(2*pi*62.5)
        d_theta = c1*45*32.5/(62.5*2)
        dx = 0
        dy = 0
        
    else:
        d_theta = 0
        dx = d_dist*cos(radians(current_pose[2]))*2
        dy = d_dist*sin(radians(current_pose[2]))*2
        
    #print(d1,dx,dy,d_theta,rotate)
    return current_pose[0] + dx,current_pose[1] + dy,current_pose[2] + d_theta*rotate*1    

def motor_control(ser,set_theta, current_pose,end_point):
        if set_theta - current_pose[2]  > 8:
            #lmotor + and rmotor -
            print("Now turning left")
            ser.write(b"0")
            rotate = 1
            
        elif set_theta - current_pose[2] < -8:
            #lmotor - and rmotor +
            print("Now turning right")
            ser.write(b"1")
            rotate = -1
            
        elif abs(current_pose[0] - end_point[0]) > 5 or abs(current_pose[1] - end_point[1]) > 5:
            #lmotor + and rmotor +
            print("Now forward")
            ser.write(b"2")
            rotate = 0
            
        else:
            #lmotor + and rmotor +
            print("Stop")
            ser.write(b"3")
            rotate = 0
        return rotate    

def main(ser,prev_x,prev_y,prev_w1,prev_w2,end_point):
    while True:
        start_time = time.time()
        ser_bytes = ser.readline().decode("utf-8").rstrip()
        data = ser_bytes.split("\r")
        print(data)
        if len(data[0]) > 6 and data[0].find('s') == -1:
            #print(data[0])
            try:
                curr_x,curr_y,curr_w1,curr_w2 = [float(i) for i in data[0].split("|")]
            except ValueError:
                curr_x,curr_y,curr_w1,curr_w2 = prev_x,prev_y,prev_w1,prev_w2
                
            global current_pose
            global rotate
            current_pose = list(get_position(curr_x-prev_x, curr_y - prev_y,curr_w1-prev_w1,curr_w2-prev_w2,current_pose,rotate,time.time() - start_time))
            
            
            if current_pose[2] > 360:
                current_pose[2] = 0;
            #print(current_pose)
            
            prev_x,prev_y,prev_w1,prev_w2 = curr_x,curr_y,curr_w1,curr_w2
            
            set_theta = degrees(arctan2((end_point[1]-current_pose[1]),(end_point[0]-current_pose[0])))
            
            if (end_point[1]-current_pose[1] < 0):
                set_theta = set_theta  + 360
            print(set_theta)
            rotate = motor_control(ser,set_theta,current_pose,end_point)    
            time.sleep(0.05)
            return [round(i,2) for i in current_pose],curr_w1,curr_w2
            break
