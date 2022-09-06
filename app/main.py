#import tkinter as tk #! linux : Tkinter #! win10 : tkinter
from tkinter import *
from tkinter import filedialog
import os,sys
from pygame import mixer
import time
import csv

### todo Fix clashing audio
### todo Timetable with choice to show classes only [not important]
### todo Pomodoro timer -
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

#? frame where everything is in
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
pomoFrame = Frame(mainFrame)
pomoFrame.grid(row=3, column=0, columnspan=5)

#root.attributes('-zoomed', True)
#root.state('zoomed')

link = opencsv('csv/link.csv')

for i in link:
    print(i[0])
    print(i[1])


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
def initClock():
    global clockDisplay, dateDisplay
    clockDisplay = Label(clockFrame, font=('Arial',30), text="HH:MM::SS")
    clockDisplay.grid(row=0, column=0, columnspan=2)
    dateDisplay = Label(clockFrame, font=('Arial',30),text="DD/MM/xaxisY")
    dateDisplay.grid(row=0, column=3, ipadx=10, columnspan=2)

    updateClock()

def updateClock():
    global cH24, cH12, cM, cS #? clock variable [Hour24 Hour12 Minute Second]
    global dD, dM, dY #? Date variable [Day Month Year]

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
isAudio = False
audio = mixer
audio.init()
audioFile = ""
audioList = []
isAudio = False
def audioPlayer():
    #TODO previous, next
    global audioLabel,listLabel,listFrame
    loadBtn = Button(audioFrame, text="Load", command=lambda:load())
    loadBtn.grid(row=1, column=0, columnspan=5)

    prevBtn = Button(audioFrame, text="Prev")
    prevBtn.grid(row=2, column=0)
    stopBtn = Button(audioFrame, text="Stop", command=lambda:stop())
    stopBtn.grid(row=2, column=1)
    playBtn = Button(audioFrame, text="Play", command=lambda:play(len(audioList)-1))
    playBtn.grid(row=2, column=2)
    pauseBtn = Button(audioFrame, text="Pause", command=lambda:pause())
    pauseBtn.grid(row=2, column=3)
    nextBtn = Button(audioFrame, text="Next")
    nextBtn.grid(row=2, column=4)

    audioLabel = Label(audioFrame, text="Audio Title",width="10")#, relief='flat'
    audioLabel.grid(row=0, column=0, columnspan=5, sticky='nesw')
    listFrame = Frame(audioFrame, width=10)
    listFrame.grid(row=4,column=0, columnspan=5)
    # listLabel = Label(listFrame, text="Playlist",height=10)
    # listLabel.grid(row=1, column=0, columnspan=5)



def load():
    global audioFile
    i = len(audioList)
    audioFile = filedialog.askopenfilename()
    audioLabel.config(text=os.path.basename(audioFile))
    audioList.append(audioFile)
    # Button(listFrame, text=audioList[i].split("/",2),command=lambda:play(i)).grid(row=i, column=0, columnspan=5)
    Button(listFrame, text=os.path.basename(audioList[i]),command=lambda:play(i)).grid(row=i, column=0, columnspan=5)
    # print(audioList)
    # print("Loading....."+audioFile)

def play(i):
    audioFile = audioList[i]
    if audioFile:
        audio.music.load(audioFile)
        audio.music.play(loops=-1)
        isAudio = True
    else:
        filenotload()

# *for local variable referenced before assignment,
# *set variable to global
# *function asssumes variable is local

def pause():
    global isAudio#:] solution for referenced before variable
    if isAudio:
        mixer.music.unpause()
    else:
        mixer.music.pause()
    isAudio = not isAudio

def stop():
    mixer.music.stop()

def filenotload():
    audioLabel.config(text="File Not Loaded")

######! END MUSIC PLAYER !######

######! START POMODORO######
timer = 0
def pomo():
    pomoStart = Button(pomoFrame, text="Set", command=lambda:setPomo(10))#! testing 3.lama sgt nk tunggu 30
    pomoStart.grid(row=0, column=0)
    global pomoCount
    pomoCount = Label(pomoFrame, text=timer)
    pomoCount.grid(row=0, column=1)
pomo()
def setPomo(t):
    global timer
    timer = timer + t
    countdown()

def countdown():
    global timer
    timer -= 1
    pomoCount.config(text=timer)
    root.after(1000,countdown)

######! END POMODORO######
if showDaily:dailyPlanner()
if showMedia:audioPlayer()
if showClock:initClock()

def refresh():
    root.after(1000,refresh)
refresh()


root.iconbitmap('./icon.ico')
root.eval('tk::PlaceWindow . center')#? Application positioned at center of screen
root.mainloop()
# global timer #? timer variable
# global playingState
# pomoSound = mixer
# if timer>0:
#     timer-=1
#     timerDisplay.config(text=timer)
# elif isRing:
#     pomoSound.init()
#     sound = "./alarm.mp3"
#     pomoSound.Channel(0).play(sound,loops=-1)
# #elif isRing==FALSE:
# #    pomoSound.music.pause()#! issue: music player also paused

# global timer, isRing
# timer=0

# pomoInput = Text(clockFrame, height="1", width="10")
# pomoInput.grid(row=0, column=9)
# snoozeBtn = Button(clockFrame, text="Snooze", command=lambda:snooze())
# snoozeBtn.grid(row=0, column=8)
# mixer.init()
# isRing = FALSE

# def countdown(t):
#     global timer,isRing
#     isRing = TRUE
#     timer = timer + t

# def snooze():
#     global isRing
#     isRing = FALSE
# timerDisplay = Label(clockFrame, font=('Arial',20), text=0)
# timerDisplay.grid(row=0, column=6)

#:] Music Player
#:] Daily Time Table
#:] Pomodoro
#:] Clock/Date