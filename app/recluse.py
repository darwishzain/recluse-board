#import tkinter as tk #! linux : Tkinter #! win10 : tkinter
from ast import For
from tkinter import *
from tkinter import filedialog
import os,sys
from pygame import mixer
import time
import csv
from wifi import Cell, Scheme

""" import subprocess
networks = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
decoded_networks = networks.decode('ascii')
print(decoded_networks) """
### todo Fix clashing audio
### todo Timetable with choice to show classes only [not important]
### todo Pomodoro timer -
whitesmoke = "#F0F0F0"
black = "#000000"
white = "#FFFFFF"
goldenpoppy = "#F3C300"
celticblue = "#2E6DB4"
persiangreen = "#00AC9F"
cadmiumred = "#DF0024"

appName = 'Recluse Board'
appPlatform = sys.platform
appOs = os.name
appDev = 'Darwish Zain'
appVer = '0.0.1 - reborn'

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
#root.attributes('-zoomed', True)
#root.state('zoomed')

#? frame where everything is in
mainFrame = Frame(root, bg=whitesmoke, height=300, width=500)
mainFrame.grid(row=0, column=0)

showFrame = Frame(mainFrame)
showFrame.grid(row=0,column=0, columnspan=5)
clockFrame = Frame(mainFrame)
clockFrame.grid(row=1, column=0,columnspan=5)
linkFrame = Frame(mainFrame)
linkFrame.grid(row=2, column=0, columnspan=5)
tableFrame = Frame(mainFrame)
tableFrame.grid(row=3, column=0)#:] 0,1,2,3,4
audioFrame = Frame(mainFrame, width="500", height="20")
audioFrame.grid(row=1, column=5, rowspan=2)

link = opencsv('csv/link.csv')

def linkButton(l):
    Button(linkFrame,text=link[l][0], command=lambda:openlink(link[l][1])).grid(row=0, column=l)

for i in range(0,len(link)):
    linkButton(i)

######! START TABLE !######
showTable = True
def table():
    tabledata = opencsv('csv/week.csv')
    for yaxis in range(8):
        for xaxis in range(25):
            day = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
            if(yaxis==0):
                if(xaxis==0):
                    tableText = "Day\Time"#column0
                else:
                    tableText = "{0:0=2d}".format(xaxis-1)+"00"
            else:
                if(xaxis==0):
                    tableText = day[yaxis-1]
                else:
                    tableText = tabledata[yaxis-1][xaxis-1]
            Label(tableFrame, justify="left", text=tableText).grid(row=yaxis, column=xaxis, ipady=5, sticky='nesw')
######! END TABLE !######
######! START CLOCK !######
def initClock():
    global clockDisplay, dateDisplay, timer, pomotime
    timer = 0
    clockDisplay = Label(clockFrame, font=('Arial',20), text="HH:MM::SS")
    clockDisplay.grid(row=0, column=0)
    dateDisplay = Label(clockFrame, font=('Arial',20),text="DD/MM/YYYY")
    dateDisplay.grid(row=0, column=1)

    pomo10 = Button(clockFrame, text="+10", command=lambda:pomo(10))
    pomo10.grid(row=0, column=3)
    pomo30 = Button(clockFrame, text="+30", command=lambda:pomo(30))
    pomo30.grid(row=0, column=4)
    pomotime = Label(clockFrame, text=timer)
    pomotime.grid(row=0, column=2)
    update()

def pomo(t):
    global timer
    timer = timer + t

def t(q):
    return time.strftime(q)

def update():
    global timer

    clock = t('%H')+":"+t('%M')+":"+t('%S')
    clockDisplay.config(text=clock)
    date = t('%d')+"/"+t('%m')+"/"+t('%Y')
    dateDisplay.config(text=date)
    pomotime.config(text=timer)
    if(timer>0):
        timer -= 1

    root.after(1000,update)

######! END CLOCK !######
#*--------------------*#
######! START MUSIC PLAYER !######
#TODO previous, next
isAudio = False
audio = mixer
audio.init()
audioFile = ""
audioList = []
def audioPlayer():
    global audioLabel,listLabel,listFrame
    loadBtn = Button(audioFrame, text="Load", command=lambda:load())
    loadBtn.grid(row=1, column=0, columnspan=5)

    prevBtn = Button(audioFrame, text="<<", state='disabled')
    prevBtn.grid(row=2, column=0)
    stopBtn = Button(audioFrame, text="Stop", command=lambda:stop())
    stopBtn.grid(row=2, column=1)
    playBtn = Button(audioFrame, text="Play", command=lambda:play(len(audioList)-1))
    playBtn.grid(row=2, column=2)
    pauseBtn = Button(audioFrame, text="Pause", command=lambda:pause())
    pauseBtn.grid(row=2, column=3)
    nextBtn = Button(audioFrame, text=">>", state='disabled')
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
    if(audioFile):
        audioLabel.config(text=os.path.basename(audioFile))
        audioList.append(audioFile)
        Button(listFrame, text=os.path.basename(audioList[i]),command=lambda:play(i)).grid(row=i, column=0, columnspan=5)

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
Button(showFrame, text='Show\nTable', command=lambda:table()).grid(row=0, column=0)
Button(showFrame, text='Hide\nTable', command=lambda:tableFrame.grid_remove()).grid(row=0, column=1)
audioPlayer()
initClock()

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