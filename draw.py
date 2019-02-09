import numpy as np
import cv2
import time
from math import *

def nothing(z):
    pass

def recenter(x,y,img,flag=""):
    rows,cols,aux = img.shape
    x += cols/4
    y += rows/2
    if (x > cols and flag != "-x"):
        x = x-cols
    if (y > rows):
        y = y-rows
    return int(x),int(y)

def draw():
    # img parameters
    w = 1400
    h = 800
    t = 0
    wave = []
    # setup the black background
    img = np.zeros((h, w, 3),np.uint8)
    # cria as barras de opcao
    cv2.namedWindow('image')
    cv2.createTrackbar('N','image',1,20,nothing)

    while(1):
        N = cv2.getTrackbarPos('N','image')
        # display the img
        cv2.imshow('image', img)
        # check for esc
        j = cv2.waitKey(1) & 0xFF
        if j == 27:
            break
        # reset the bg
        img = np.zeros((h, w, 3),np.uint8)

######### magic happens here #################################

        k = 150
        cx,cy = recenter(0,0,img)
        x = 0
        y = 0
        prevx = cx
        prevy = cy
        for i in range(N):
            n = i*2+1
            radius = k*4 / (n * pi)
            x += radius * cos(n*t)
            y += radius * sin(n*t)
            cv2.circle(img,(prevx,prevy), int(radius), (255,255,255), 1) # circle draw
            rx,ry = recenter(x,y,img)
            cv2.line(img,(prevx,prevy),(rx,ry),(255,0,0),2)
            prevx, prevy = recenter(x,y,img)
        # cleaning wave list
        if (len(wave)>1000):
            del wave[len(wave)-1]
        wave.insert(0,y) # shift to the right and append value on index 0
        x,y = recenter(x,y,img,"-x") # position of the end dot
        cv2.circle(img,(x,y),3,(0,0,255),-1)
        # wave draw
        prvx = x
        prvy = y
        aux = range(len(wave)-1)
        for i in aux:
            rcx,rcy = recenter(i+250,wave[i],img,"-x")
            cv2.line(img,(prvx,prvy),(rcx,rcy),(255,255,255),2)
            #cv2.circle(img,(rcx,rcy),2,(255,255,255),-1)
            prvx = rcx
            prvy = rcy

##############################################################

        # function time count
        t -= 0.01

draw()
