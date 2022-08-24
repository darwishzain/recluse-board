#import tkinter as tk #! linux : Tkinter #! win10 : tkinter
from mimetypes import init
from tkinter import *
from tkinter import filedialog
import os,sys
from pygame import mixer
import time
import csv

### TODO Fix clashing audio
### TODO Timetable with choice to show classes only [not important]
### TODO Pomodoro timer -
light_color = "#F0F0F0"
dark_color = "#000000"

appName = 'Recluse Board'
appPlatform = sys.platform
appOs = os.name
appDev = 'Darwish Zain'
appVer = '0.0.1 - reborn'

showDaily = True
showMedia = True
showClock = True

def appInfo():
    print("Running "+appName+" on "+appPlatform)
    time.sleep(1)
    print("Developed by "+appDev)
    time.sleep(1)
    print("Version "+appVer)
    time.sleep(1)

#appInfo()
def command(cmd):
    os.system(str(cmd))

def openlink(link):
    if os.name == 'posix':
        link='xdg-open '+link
    elif os.name == 'nt':
        link = 'explorer '+link
    os.system(str(link))

def opencsv(thefile):
    filedata = []
    if thefile:
        with open(thefile,'r') as o:
            reader = csv.reader(o)
            for row in reader:
                filedata.append(row)
            return filedata

root = Tk()
root.title(appName+" v"+appVer+" on "+appPlatform)
#root.geometry("1350x400")

#? frame where the everything is in
mainFrame = Frame(root, bg='#F0F0F0', height=300, width=500)
mainFrame.grid(row=0, column=0)

titleFrame = Frame(mainFrame, bg='#FFF')
titleFrame.grid(row=0, column=4, columnspan=5)
clockFrame = Frame(mainFrame)
clockFrame.grid(row=1, column=0)
tableFrame = Frame(mainFrame)
tableFrame.grid(row=2, column=0, columnspan=5)#0,1,2,3,4
audioFrame = Frame(mainFrame, bg='#FFF', width="500", height="20")
audioFrame.grid(row=2, column=5)
cTFrame = Frame(mainFrame)
cTFrame.grid(row=3, column=0, columnspan=5)

#root.attributes('-zoomed', True)
#root.state('zoomed')

link = opencsv('csv/link.csv')
print(len(link))

######! START TABLE !######
def dailyPlanner():
    dailydata = opencsv('csv/daily.csv')
    for yaxis in range(8):
        for xaxis in range(25):
            day = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
            #today = time.strftime("%A") #? return day
            #now = time.strftime("%H") #? sreturn hour
            if(yaxis==0):
                if(xaxis!=0):
                    #? time of the day
                    tableText = "{0:0=2d}".format(xaxis-1)+"00"
                else:
                    tableText = "Day\Time"
            else:
                if(xaxis==0):
                    #if(today == day[yaxis-1]):
                    #    tablebg = "#00FF00"
                    tableText = day[yaxis-1]
                else:
                    #if(today == day[yaxis-1] and now == "{0:0=2d}".format(xaxis)):
                    #    tablebg = "#00FF00"
                    #    tablefg = "#0F0F0F"
                    tableText = dailydata[yaxis-1][xaxis-1]
            Label(tableFrame, justify="left", bg=light_color, fg=dark_color, text=tableText).grid(row=yaxis, column=xaxis, ipady=5, sticky='nesw')

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
    pomoInput = Text(clockFrame, height="1", width="10")
    pomoInput.grid(row=0, column=9)
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
    global cH24, cH12, cM, cS #? clock variable [Hour24 Hour12 Minute Second]
    global dD, dM, dY #? Date variable [Day Month Year]
    global timer #? timer variable
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
isAudio = False
audio = mixer
audio.init()
audioFile = ""
audioList = []
def audioPlayer():
    global audioLabel
    loadBtn = Button(audioFrame, text="Load", command=lambda:load())
    loadBtn.grid(row=0, column=0, columnspan=5)

    prevBtn = Button(audioFrame, text="Prev")
    prevBtn.grid(row=2, column=0)
    stopBtn = Button(audioFrame, text="Stop", command=lambda:stop())
    stopBtn.grid(row=2, column=1)
    playBtn = Button(audioFrame, text="Play", command=lambda:play())
    playBtn.grid(row=2, column=2)
    pauseBtn = Button(audioFrame, text="Pause", command=lambda:pause())
    pauseBtn.grid(row=2, column=3)
    nextBtn = Button(audioFrame, text="Next")
    nextBtn.grid(row=2, column=4)

    audioLabel = Label(audioFrame, text="Audio Title",width="10")#, relief='flat'
    audioLabel.grid(row=3, column=0, columnspan=5, sticky='nesw')
    listFrame = Frame(audioFrame)
    listFrame.grid(row=4,column=0, columnspan=5)
    listLabel = Label(listFrame, text="What",width=10,height=20)
    listLabel.grid(row=5, column=0, columnspan=5)



def load():
    global audioFile
    audioFile = filedialog.askopenfilename()
    audioLabel.config(text=audioFile)
    audioList.append(audioFile)
    print(audioList)
    print("Loading....."+audioFile)

def play():
    global isAudio
    if audioFile:
        audio.music.load(audioFile)
        audio.music.play(loops=-1)
        isAudio = True
    else:
        filenotload()
def pause():
    global isAudio
    if not isAudio:
        mixer.music.pause()
        isAudio=True
    else:
        mixer.music.unpause()
        isAudio = False
def stop():
    mixer.music.stop()

def filenotload():
    audioLabel.config(text="File Not Loaded")

######! END MUSIC PLAYER !######

if showDaily:dailyPlanner()
if showMedia:audioPlayer()
if showClock:initClock()

root.iconbitmap('./icon.ico')
root.eval('tk::PlaceWindow . center')#? Application positioned at center of screen
root.mainloop()
#:] Music Player
#:] Daily Time Table
#:] Pomodoro
#:] Clock/Date