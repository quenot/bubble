#!/usr/bin/env python
# coding: utf-8

# Chargement du module tkinter
import os
from tkinter import * # pour Python2 se serait Tkinter
from tkinter import filedialog
from PIL import ImageTk,Image
import math
import numpy as np
import csv
import matplotlib.image as mpimg
import qbubble as qb
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def GenerateMask():
    global b
    h = imgH
    w = imgW
    outimg = np.zeros((h, w), dtype = 'uint8')
    for v in lv:
        a = qb.qbubbleImageInside(v,w,h).astype(np.uint8)
        outimg= a|outimg
    
    # Save the output image
    path = tmpimgpath.replace(".png","").replace(".jpg","")
    plt.imsave(path +'_mask.png', outimg, cmap=cm.gray)

def original():
    global b
    global lv
    lv = lv_orig.copy()
    b = bubblePlot(lv,s=1)
    Drawbubbles()

def Undo():
    if len(Canevas.find_all()) > 1:
        item = Canevas.find_all()[-1]
        Canevas.delete(item)

def EffacerTout():
    while len(Canevas.find_all()) > 1:
        Undo()

def asignColor(input=1):
    #0 = unselected, 1 = selected, 2 = selected for fix
    if(input==0):
        return ['#0ff','']
    elif(input==1 ):
        return ['#f00','#f00']
    elif(input==2):
        return ['#00f','#00f']

def Drawbubbles():
    #draws all the contours on the canvas
    EffacerTout()
    for bubble in b:
        i=0
        cbub = asignColor(bubble[2])
        ps=[]
        while i < len( bubble[1]):
            #line = Canevas.create_line(ratio*bubble[0][i][0],ratio*bubble[0][i][1]
            #,ratio*bubble[0][i+1][0],ratio*bubble[0][i+1][1], fill="red")
            ps.append(bubble[1][i][1]*(displayW/imgW)+ht-0.5)
            ps.append(bubble[1][i][0]*(displayH/imgH)+ht-0.5)
            i+=1
        if(len(ps)>0):
            Canevas.create_polygon(ps, outline=cbub[0],fill=cbub[1], width=pw)

def Distance(x1,y1,x2,y2):
    #euclidean distance
    return math.sqrt((math.pow(x1-x2,2))+(math.pow(y1-y2,2)))

def Key(event):
    #when user press d, the selected bubbles (b[2]=1) are removed 
    global b
    global lv
    index = len(b)
    while index>0:
        if b[index-1][2]==1:
            b.pop(index-1)
            lv.pop(index-1)
        index-=1
    Drawbubbles()

def Clic(event):
    #when there is a clic on the canvas, the bubble with the closest center will be selected
    X = (event.x-ht)/(displayW/imgW)
    Y = (event.y-ht)/(displayH/imgH)
     
    distance= 99999.9
    for bubble in b:
        distanceaux = Distance(bubble[0][0],bubble[0][1],X,Y)
        if distanceaux<distance:
            distance = distanceaux
            bubblesel = bubble

    if(bubblesel[2]==0):
        bubblesel[2]=1
    elif(bubblesel[2]==1):
        bubblesel[2]=0
    Drawbubbles()

def bubblePlot(lv, s=1):
    #build the contours from the armonics
    bubbles=[]
    for v in lv:
        points = qb.qbubbleTkPolygon(s*v)
        bubbles.append([v,points,0])
    return bubbles

lv = []         # list of bubble parameters
b  = []         # list of bubble points and properties
displayH = 550  # size of the image to be displayed
displayW = 550  
imgH = 0        # original size of the image
imgW = 0
pw = 2.5        # polygon drawing width

# By default, canvas' highlightthickness is set to 2,
# which causes inappropriate shifts of images and contours.
# This is now handled and ht can be set to any (positive int) value.
ht = 10

# Building the main window
root = Tk()
root.title('Bubble')
root.state("normal")
# grid
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=6)
root.columnconfigure(1, weight=2)
root.columnconfigure(1, weight=2)

frame = Frame(root)         # , padding="3 3 12 12")
frame.grid(column=0, row=0) # frame.config(padx = 0, pady = 0, bd = 0)

# open an image
tmpimgpath = filedialog.askopenfilename(initialdir=os.getcwd(),filetypes=[("Image files", ".jpg .png")])
inputImg=Image.open(tmpimgpath)
filename = os.path.basename(tmpimgpath).replace(".png","").replace(".jpg","")
imgH = inputImg.height
imgW = inputImg.width
imgp = inputImg.resize([displayH, displayW])
photo = ImageTk.PhotoImage(imgp)

#open the csv file asociated to the image
csvf = tmpimgpath.replace(".png",".csv").replace(".jpg",".csv")
with open(csvf, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        lv.append(np.array(row, dtype=np.float32))
        
# save the original data in case of mistake
lv_orig = lv.copy()

# build the curves using the parameters in the csv file
b = bubblePlot(lv,s = 1)

# creation of canvas to put the image and the contours
Canevas = Canvas(frame,width = photo.width(), height = photo.height(), highlightthickness = ht)
item = Canevas.create_image(ht, ht, anchor=NW, image=photo)

Drawbubbles()

Canevas.bind('<Button-1>', Clic)
root.bind('<Key>', Key)
Canevas.grid(row=0, column=0)

qbu = Button(root, text='Original', command=original)
qb2 = Button(root, text='Save mask', command=GenerateMask)

qbu.grid(row=0, column=1)
qb2.grid(row=0, column=2)

#to be sure the program will catch all the events
root.focus_force()

root.mainloop()

