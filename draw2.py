import numpy as np
import cv2
import time
import random
from math import *
import json


def map(value, start1, stop1, start2, stop2):
    # adapted from:
    # https://forum.processing.org/two/discussion/22471/how-does-mapping-function-work
    outgoing = start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1));
    badness = None;
    if (outgoing != outgoing):
        badness = "NaN (not a number)"
    elif (isinf(outgoing)):
        badness = "infinity";

    if (badness != None):
        print("infinity error")
        return None

    return outgoing;

def epiCycles(x,y,offset,fourier,t,img):
        cx,cy = recenter(x,y,img, "-x")
        prevx = cx
        prevy = cy
        for i in range(len(fourier)):
            freq = fourier[i]["freq"]
            radius = fourier[i]["amp"]
            phase = fourier[i]["phase"]
            x +=  radius * cos(freq*t + phase + offset)
            y +=  radius * sin(freq*t + phase + offset)
            cv2.circle(img,(prevx,prevy), int(radius), (255,255,255), 1) # circle draw
            rx,ry = recenter(x,y,img,"-x")
            cv2.line(img,(prevx,prevy),(rx,ry),(255,0,0),2)
            prevx, prevy = recenter(x,y,img,"-x")
        x,y = recenter(x,y,img,"-x") # position of the end dot
        cv2.circle(img,(x,y),3,(0,0,255),-1)
        return x,y

def dft(x):
    X = []
    N = len(x)
    for k in range(N):
        re = 0
        im = 0
        for n in range(N):
            phi = (2*pi*k*n)/N
            re += x[n] * cos(phi)
            im -= x[n] * sin(phi)
        re = re/N
        im = im/N

        freq  = k
        amp   = sqrt(re*re+im*im)
        phase = atan2(im,re)
        X.append({"re":re,"im":im,"freq":freq,"amp":amp,"phase":phase})
    return X

def recenter(x,y,img,flag=""):
    rows,cols,aux = img.shape
    if (flag == "-b"):
        x -= cols/4
        y -= rows/2
    else:
        x += cols/4
        y += rows/2
    if (x > cols and flag != "-x"):
        x = x-cols
    if (y > rows and flag != "-x"):
        y = y-rows
    return int(x),int(y)

def draw():
    signalX = []
    signalY = []

    # uncoment for circle #################################################################
    # for i in range(100):
    #     angle = map(i,0,100,0,pi*2)
    #     signalX.append(125*cos(angle))
    #     signalY.append(125*sin(angle))
    #######################################################################################

    # uncoment for code_train logo ########################################################
    # with open('codingtrain.json') as data_file:
    #     data = json.load(data_file)
    # signalX = [data["drawing"][i*3]['x'] for i in range(int(len(data["drawing"])/3))]
    # signalY = [data["drawing"][i*3]['y'] for i in range(int(len(data["drawing"])/3))]
    #######################################################################################

    # uncoment for hearth draw ############################################################
    t = 2
    while t <= 40:
        x = 4*(16*(sin(t))**3)
        y = -4*(13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t))
        signalX.append(x)
        signalY.append(y)
        t = t+0.05
    #######################################################################################

    # Calculating dft
    fourierX = dft(signalX)
    fourierY = dft(signalY)

    # Sorting circles in radius order
    fourierX = sorted(fourierX, key=lambda k: k["amp"], reverse = True)
    fourierY = sorted(fourierY, key=lambda k: k["amp"], reverse = True)

    # img parameters
    w = 1400
    h = 800
    t = 0
    path = []
    # setup the black background
    img = np.zeros((h, w, 3),np.uint8)

    while(1):
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
        x = 0
        y = 0

        x1, y1 = epiCycles(400,-300,0,fourierX,t,img)
        x2, y2 = epiCycles(0,0,pi/2,fourierY,t,img)
        #cleaning wave list
        if (len(path)>10000):
            del path[len(path)-1]
        path.insert(0,(x1,y2)) # shift to the right and append value on index 0
        prvx = path[0][0]
        prvy = path[0][1]
        cv2.line(img,(x1,y1),(path[0][0],path[0][1]),(0,255,0),1)
        cv2.line(img,(x2,y2),(path[0][0],path[0][1]),(0,255,0),1)
        cv2.circle(img,(path[0][0],path[0][1]),5,(0,0,255),-1)
        for i in range(len(path)):
            cv2.line(img,(prvx,prvy),(path[i][0],path[i][1]),(255,255,255),2)
            prvx = path[i][0]
            prvy = path[i][1]

##############################################################

        # function time count
        dt = 2*pi / len(fourierY)
        t -= dt
        #time.sleep(0.01)

draw()
