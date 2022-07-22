#import tkinter as tk #! linux : Tkinter #! win10 : tkinter
from tkinter import *
from tkinter import filedialog
import os,sys
from pygame import mixer
import time
import csv
### TODO Fix clashing audio
### TODO Timetable with choice to show classes only [not important]
### TODO Pomodoro timer -

appName = 'Recluse Board'
appPlatform = sys.platform
appOs = os.name
appDev = 'Darwish Zain'
appVer = '0.0.1 - reborn'

def appInfo():
    print("Running "+appName+" on "+appPlatform)
    time.sleep(1)
    print("Developed by "+appDev)
    time.sleep(1)
    print("Version "+appVer)
    time.sleep(1)

appInfo()

root = Tk()
root.title(appName+" v"+appVer+" on "+appPlatform)
#root.geometry("1350x400")


#? frame where the button is in
mainFrame = Frame(root, bg='#F0F0F0', height=300, width=500)
mainFrame.grid(row=0, column=0)
titleFrame = Frame(mainFrame, bg='#FFF')
titleFrame.grid(row=0, column=4, columnspan=5)
clockFrame = Frame(mainFrame, bg="#FFF")
clockFrame.grid(row=1, column=0)
tableFrame = Frame(mainFrame)
tableFrame.grid(row=2, column=0, columnspan=5)
cTFrame = Frame(mainFrame)
cTFrame.grid(row=3, column=0, columnspan=5)
mediaFrame = Frame(mainFrame, bg='#FFF', width="500", height="20")
mediaFrame.grid(row=5, column=0, columnspan=3)
#root.attributes('-zoomed', True)
#root.state('zoomed')

######! START TABLE !######
def dailyPlanner():
    global tdata
    tdata = []
    dailyfile = './csv/daily.csv'
    if dailyfile:
        with open(dailyfile,'r') as tcsv:
            treader = csv.reader(tcsv)
            for row in treader:
                tdata.append(row)
        for yaxis in range(8):
            for xaxis in range(25):
                tableBg = "#F0F0F0"
                tableFg = "#000000"
                day = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
                #today = time.strftime("%A") #? return day
                #now = time.strftime("%H") #? sreturn hour
                if(yaxis==0):
                    if(xaxis!=0):
                        #* time of the day
                        tableText = "{0:0=2d}".format(xaxis-1)+"00"
                    else:
                        tableText = "Day\Time"
                else:
                    if(xaxis==0):
                        #if(today == day[yaxis-1]):
                        #    tableBg = "#00FF00"
                        tableText = day[yaxis-1]
                    else:
                        #if(today == day[yaxis-1] and now == "{0:0=2d}".format(xaxis)):
                        #    tableBg = "#00FF00"
                        #    tableFg = "#0F0F0F"
                        tableText = tdata[yaxis-1][xaxis-1]
                Label(tableFrame, justify="left", bg=tableBg, fg=tableFg, text=tableText).grid(row=yaxis, column=xaxis, ipady=5, sticky='nesw')

dailyPlanner()
######! END TABLE !######

######! START CLOCK !######
isRing = FALSE
def initClock():
    global clockDisplay, dateDisplay, timerDisplay
    global timer, isRing
    timer=0
    clockDisplay = Label(clockFrame, font=('Arial',30), text="HH:MM::SS")
    clockDisplay.grid(row=0, column=0, columnspan=2)
    dateDisplay = Label(clockFrame, font=('Arial',30),text="DD/MM/xaxisY")
    dateDisplay.grid(row=0, column=3, ipadx=10, columnspan=2)
    timerDisplay = Label(clockFrame, font=('Arial',20), text=0)
    timerDisplay.grid(row=0, column=6)
    pomoThirty = Button(clockFrame, text="+30s", command=lambda:countdown(3))#! testing 3.lama sgt nk tunggu 30
    pomoThirty.grid(row=0, column=7)
    snoozeBtn = Button(clockFrame, text="Snooze", command=lambda:snooze())
    snoozeBtn.grid(row=0, column=8)
    mixer.init()

    updateClock()


def countdown(t):
    global timer,isRing
    isRing = TRUE
    timer = timer + t

def snooze():
    global isRing
    isRing = FALSE

def updateClock():
    global cH24, cH12, cM, cS #* clock variable [Hour24 Hour12 Minute Second]
    global dD, dM, dY #* Date variable [Day Month Year]
    global timer #* timer variable
    global playingState
    pomoSound = mixer

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
    if timer>0:
        timer-=1
        timerDisplay.config(text=timer)
    elif isRing:
        pomoSound.init()
        sound = "./alarm.mp3"
        pomoSound.Channel(0).play(sound,loops=-1)
    #elif isRing==FALSE:
    #    pomoSound.music.pause()#! issue: music player also paused

    root.after(1000,updateClock)

######! END CLOCK !######
#*--------------------*#
######! START MUSIC PLAYER !######
def mediaPlayer():
    global songLabel
    loadBtn = Button(mediaFrame, text="Load", command=lambda:load())
    loadBtn.grid(row=0, column=0, columnspan=5)

    prevBtn = Button(mediaFrame, text="Prev")
    prevBtn.grid(row=2, column=0)
    stopBtn = Button(mediaFrame, text="Stop", command=lambda:stop())
    stopBtn.grid(row=2, column=1)
    playBtn = Button(mediaFrame, text="Play", command=lambda:play())
    playBtn.grid(row=2, column=2)
    pauseBtn = Button(mediaFrame, text="Pause", command=lambda:pause())
    pauseBtn.grid(row=2, column=3)
    nextBtn = Button(mediaFrame, text="Next")
    nextBtn.grid(row=2, column=4)
    songLabel = Label(mediaFrame, text="Audio Title")#, relief='flat'
    songLabel.grid(row=3, column=0, columnspan=5, sticky='nesw')


def load():
    global musicFile
    musicFile = filedialog.askopenfilename()
    songLabel.config(text=musicFile)
    print("Loading....."+musicFile)
def play():
    global playingState
    if musicFile:
        musicSound = mixer
        musicSound.init()
        musicSound.music.load(musicFile)
        musicSound.music.play(loops=-1)
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
#darwish Music Player
#darwish Daily Time Table
#darwish Pomodoro
#darwish Clock/Date