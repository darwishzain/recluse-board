#import tkinter as tk #! linux : Tkinter #! win10 : tkinter
from tkinter import *
from tkinter import filedialog
import os,sys
from pygame import mixer
import time
import csv

appName = 'Recluse Board'
appPlatform = sys.platform
appOs = os.name
appDev = 'Darwish Zain'
appVer = '0.0.1 - reborn'

def terminalLoad():
    print("Running "+appName+" on "+appPlatform)
    time.sleep(1)
    print("Developed by "+appDev)
    time.sleep(1)
    print("Version "+appVer)
    time.sleep(1)

terminalLoad()

root = Tk()
root.title(appName+" v"+appVer+" on "+appPlatform)
#root.geometry("1350x400")


#? frame where the button is in
mainFrame = Frame(root, bg='#F0F0F0', height=300, width=500)
mainFrame.grid(row=0, column=0)
titleFrame = Frame(mainFrame, bg='#FFF')
titleFrame.grid(row=0, column=4, columnspan=5)
cFrame = Frame(mainFrame, bg="#FFF")
cFrame.grid(row=1, column=0)
tFrame = Frame(mainFrame)
tFrame.grid(row=2, column=0, columnspan=5)
mFrame = Frame(mainFrame, bg='#FFF', width="500", height="20")
mFrame.grid(row=5, column=0, columnspan=3)
#root.attributes('-zoomed', True)
#root.state('zoomed')

######! START TABLE !######
def timeTable():
    global tValue
    tValue = []
    tFile = './csv/table.csv'
    with open(tFile,'r') as tCsv:
        tReader = csv.reader(tCsv)
        for row in tReader:
            tValue.append(row)
    for x in range(7):
        for y in range(24):
            Label(tFrame, bg=tValue[x][25], text=tValue[x][y]).grid(row=x, column=y, ipadx=5, ipady=5, sticky='nesw')

#            tItem = tValue[x][y]
#            if tItem == "Free":
#                Label(tFrame, text=tItem, bg="#00AC9F", fg="#000000").grid(row=x, column=y)
#            elif tItem == "Sleep":
#                Label(tFrame, text=tItem, bg="#000000", fg="#FFFFFF").grid(row=x, column=y)
#            else:
#                Label(tFrame, text=tItem).grid(row=x, column=y)

timeTable()


######! END TABLE !######
######! START CLOCK !######
def initClock():
    global clockDisplay, dateDisplay
    clockDisplay = Label(cFrame, font=('Arial',30), text="HH:MM::SS")
    clockDisplay.grid(row=0, column=0, columnspan=2)
    dateDisplay = Label(cFrame, font=('Arial',30),text="DD/MM/YYYY")
    dateDisplay.grid(row=0, column=3, ipadx=10, columnspan=2)
    updateClock()

def updateClock():
    global cH24, cH12, cM, cS
    global dD, dM, dY
    cH24 = time.strftime("%H")
    cH12 = time.strftime("%I")
    cM = time.strftime("%M")
    cS = time.strftime("%S")
    dD  = time.strftime("%d")
    dM  = time.strftime("%m")
    dY  = time.strftime("%Y")

    clock = cH24+":"+cM+":"+cS
    clockDisplay.config(text=clock)
    date = dD+"/"+dM+"/"+dY
    dateDisplay.config(text=date)
    root.after(1000,updateClock)
######! END CLOCK !######
#*--------------------*#
######! START MUSIC PLAYER !######
def mediaPlayer():
    global songLabel
    loadBtn = Button(mFrame, text="Load", command=lambda:load())
    loadBtn.grid(row=0, column=0, columnspan=5)

    prevBtn = Button(mFrame, text="Prev")
    prevBtn.grid(row=2, column=0)
    stopBtn = Button(mFrame, text="Stop", command=lambda:stop())
    stopBtn.grid(row=2, column=1)
    playBtn = Button(mFrame, text="Play", command=lambda:play())
    playBtn.grid(row=2, column=2)
    pauseBtn = Button(mFrame, text="Pause", command=lambda:pause())
    pauseBtn.grid(row=2, column=3)
    nextBtn = Button(mFrame, text="Next")
    nextBtn.grid(row=2, column=4)
    songLabel = Label(mFrame, text="Audio Title")#, relief='flat'
    songLabel.grid(row=3, column=0, columnspan=5, sticky='nesw')


def load():
    global musicFile
    musicFile = filedialog.askopenfilename()
    songLabel.config(text=musicFile)
    print("Loading....."+musicFile)
def play():
    global playingState
    if musicFile:
        mixer.init()
        mixer.music.load(musicFile)
        mixer.music.play(loops=-1)
def pause():
    if not playingState:
        mixer.music.pause()
        playingState=True
    else:
        mixer.music.unpause()
        playingState = False
def stop():
    mixer.music.stop()
######! END MUSIC PLAYER !######


initClock()
mediaPlayer()

#root.iconbitmap('./image/UMP-link.ico')
root.eval('tk::PlaceWindow . center')#? Application positioned at center of screen
root.mainloop()
