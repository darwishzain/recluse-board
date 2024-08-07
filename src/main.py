import calendar,csv,json,os,requests,sys,time,webbrowser
import tkinter as tk
from tkinter import Label,Frame,Button,filedialog,Entry,Scale,messagebox
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']="hide"
from pygame import mixer
#from PIL import Image, ImageTk


#? linux : Tkinter #? win10 : tkinter
#if os.name == 'posix':
#    import tkinter as tk
#    from tkinter import filedialog
#elif os.name == 'nt':
#    import tkinter as tk
#    from tkinter import filedialog
##from wifi import Cell, Scheme

""" import subprocess
networks = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
decoded_networks = networks.decode('ascii')
print(decoded_networks) """
### todo Fix clashing  pomo+ audio
### todo Timetable with choice to show classes only [not important]

color1 = "#4679c6"
color2 = "#2f54aa"
color3 = "#020a72"
color4 = "#073763"
colorb = "#000000"
colorw = "#FFFFFF"
colorws = "#F0F0F0"

def absolutepath(relative_path):
        script_dir = os.path.dirname(__file__)
        return os.path.join(script_dir, relative_path)

def loadconfig(filename=absolutepath('./config.json')):
    with open(filename, 'r') as file:
        return json.load(file)
config = loadconfig()

def editor(dir):
    #webbrowser.open(os.getcwd() + dir)
    webbrowser.open(absolutepath(dir))

def command(command):
    os.system(str(command))
class RecluseBoard:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{config['appname']} v{config['version']}-{config['name']} on {sys.platform}")
        self.root.geometry(config['windowsize'])
        self.root.attributes('-zoomed', True)
        self.root.eval('tk::PlaceWindow . center')#? Application positioned at center of screen

        #self.root.state('zoomed')
        #self.root.iconbitmap(absolutepath('./image/icon.ico'))
        #print(os.listdir("."))

        self.audiolist = []
        self.audiofile = ""
        self.initui()
        self.initclock()
        self.initaudioplayer()
        #self.seeker.set(0)


    def openfile(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.welcomelabel.config(text="Selected file: " + os.path.basename(self.file_path))

    def initui(self):
        self.baseframe = Frame(self.root)
        self.baseframe.pack()

        self.toolbar = Frame(self.baseframe)
        self.toolbar.pack(anchor="w")
        self.editlink = Button(self.toolbar, text="Links", command=lambda:editor(config['csvfile']['link'])).grid(row=0, column=0)
        self.editshortcut = Button(self.toolbar, text="Shortcuts", command=lambda:editor(config['csvfile']['shortcut'])).grid(row=0, column=1)
        self.editschedule = Button(self.toolbar, text="Schedule", command=lambda:editor(config['csvfile']['week'])).grid(row=0, column=2)
        #Button(viewFrame, text='Schedule', borderwidth=0, command=lambda:table()).grid(row=0, column=0)

        # Add other UI elements here
        self.welcomelabel = Label(self.baseframe, text="Welcome to "+config['appname'], font=("Arial", 18))
        self.welcomelabel.pack(pady=20)

        self.buttonframe = Frame(self.baseframe)
        self.buttonframe.pack()
        #self.button1 = Button(self.baseframe, text="Open File", command=self.openfile)
        #self.button1.pack()
        self.linkframe = Frame(self.buttonframe)
        self.linkframe.grid(row=0,column=0)
        self.initbutton('./csv/link.csv',self.linkframe)
        self.shortcutframe = Frame(self.buttonframe)
        self.shortcutframe.grid(row=1,column=0)
        self.initbutton('./csv/shortcut.csv',self.shortcutframe)

    def readcsv(self,filename):
        filedata = []
        if filename:
            absolutefilepath = absolutepath(filename)
            with open(absolutefilepath,'r') as o:
                reader = csv.reader(o)
                for row in reader:
                    filedata.append(row)
                return filedata

    def openurl(self,url):
        if os.name == 'posix':
            url ='xdg-open '+url
        elif os.name == 'nt':
            url = 'explorer '+url
        os.system(str(url))

    def addbutton(self,csvline,currentrow,parent,file,maxcolumn):
        currentcolumn = csvline%maxcolumn
        if(currentcolumn==0): currentrow+=1
        Button(parent, text=file[csvline][0], command=lambda:self.openurl(file[csvline][1])).grid(row=currentrow, column=currentcolumn,padx=3,pady=3)
        return currentrow

    def initbutton(self,dir,parent):
        csvfile = self.readcsv(absolutepath(dir))
        #line = len(csvfile)
        row = 0
        csvline = 0
        while(len(csvfile)>csvline):
            row = self.addbutton(csvline,row,parent,csvfile,5)
            csvline+=1

#? START audioplayer
    #TODO FIX prevbtn,nextbtn
    def initaudioplayer(self):
        self.audioframe = Frame(self.root)
        self.audioframe.pack()

        self.audiolabel = Label(self.audioframe, text="Audio Title")
        self.audiolabel.grid(row=0, column=0, columnspan=5)

        #self.seeker = ttk.Scale(self.audioframe, from_=0, to=100, orient=tk.HORIZONTAL)
        #self.seeker.grid(row=1, column=0,fill=tk.X, padx=10, pady=10)
        #self.seeker = Scale(self.audioframe, from_=0, to=100, orient=tk.HORIZONTAL,sliderlength=10,length=400)
        #self.seeker.grid(row=1, column=1,columnspan=5,padx=10, pady=10)
        #duration = mixer.Sound.get_length()

        #self.duration = self.sound.get_length()  # Duration of the audio file in seconds
        #self.channels = self.sound.get_num_channels()  # Number of audio channels (mono or stereo)
        #self.samplerate = self.sound.get_samplerate()  # Sample rate of the audio file

        self.loadbtn = Button(self.audioframe, text="Load", command=self.loadaudio)
        self.loadbtn.grid(row=2, column=1, columnspan=5)

        self.prevbtn = Button(self.audioframe, text="Prev", command=self.playaudio)
        self.prevbtn.grid(row=3, column=1)
        self.playbtn = Button(self.audioframe, text="Play", command=self.playaudio)
        self.playbtn.grid(row=3, column=2)
        self.pausebtn = Button(self.audioframe, text="Pause", command=self.pauseaudio)
        self.pausebtn.grid(row=3, column=3)
        self.stopbtn = Button(self.audioframe, text="Stop", command=self.stopaudio)
        self.stopbtn.grid(row=3, column=4)
        self.nextbtn = Button(self.audioframe, text="Next", command=self.playaudio)
        self.nextbtn.grid(row=3, column=5)

        self.playlistlabel = Label(self.audioframe, wraplength=500)
        self.playlistlabel.grid(row=4,column=0, columnspan=5)
        self.isaudioplaying = False

    def loadaudio(self):
        self.audiofile = filedialog.askopenfilename()
        if self.audiofile:
            self.audiolabel.config(text=os.path.basename(self.audiofile))
            self.audiolist.append(self.audiofile)

    def playaudio(self):
        if self.audiofile:
            mixer.init()
            mixer.music.load(self.audiofile)
            mixer.music.play()
            self.isaudioplaying = True

    def pauseaudio(self):
        if self.isaudioplaying:
            mixer.music.pause()
            self.isaudioplaying = False
        else:
            mixer.music.unpause()
            self.isaudioplaying = True

    def stopaudio(self):
        mixer.music.stop()
        self.isaudioplaying = False
#? END audioplayer
    #def onseek(self,value):
    #    position = int(value)
    #    # Update the playback position based on the seeker value
    #    # Update your audio or video playback position using 'position'
#? START clock
    #TODO FIX pomodoro sound
    def returntime(self,query):
        return time.strftime(query)

    def returnpomodoro(self, seconds):
        pomodorominutes = "{:02d}".format(seconds // 60)
        pomodoroseconds = "{:02d}".format(seconds % 60)
        return str(pomodorominutes) + ":" + str(pomodoroseconds)

    def setpomo(self,timer):
        self.pomotimer = timer

    def initclock(self):
        #TODO FIX calendar
        self.clockframe = Frame(self.baseframe)
        self.clockframe.pack()

        self.calendarframe = Frame(self.clockframe)
        self.calendarframe.pack()

        self.calendarlabel = Label(self.calendarframe, text=calendar.month(int(self.returntime('%Y')),int(self.returntime('%m'))), font=("Arial",12))
        self.calendarlabel.pack(anchor="w")
        self.pomotimer = 0
        self.clocklabel = Label(self.clockframe, text="00:00:00",font=("Arial", 18))
        self.clocklabel.pack()

        self.datelabel = Label(self.clockframe, text="00/00/0000",font=("Arial", 18))
        self.datelabel.pack()

        self.pomodoroframe = Frame(self.clockframe)
        self.pomodoroframe.pack()
        self.pomodorolabel = Label(self.pomodoroframe, text="00:00",font=("Arial", 18))
        self.pomodorolabel.grid(row=0,column=0)
        self.pomodoro30 = Button(self.pomodoroframe, text="+30", command=lambda:self.setpomo(30))
        self.pomodoro30.grid(row=0, column=1)
        self.pomodoro60 = Button(self.pomodoroframe, text="+60", command=lambda:self.setpomo(60))
        self.pomodoro60.grid(row=0, column=2)
        #self.pomoinput = Entry(self.pomodoroframe, textvariable=30, width=3)
        #self.pomoinput.grid(row=0, column=3)
        #self.pomoinputset = Button(self.pomodoroframe, text="Pomo")
        #self.pomoinputset.grid(row=0, column=4)
        #self.pomoinput.insert(self.END,"25")
        self.pomodoro00 = Button(self.pomodoroframe, text="Reset", command=lambda:self.setpomo(0) )
        self.pomodoro00.grid(row=0, column=5)

        self.updateclock()

    def updateclock(self):
        clockstr = self.returntime('%H')+":"+self.returntime('%M')+":"+self.returntime('%S')
        datestr = self.returntime('%d')+"/"+self.returntime('%m')+"/"+self.returntime('%Y')
        pomodorostr = self.returnpomodoro(self.pomotimer)
        if(self.pomotimer>0):
            self.pomotimer-=1
        #timestr = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.clocklabel.config(text=clockstr)
        self.datelabel.config(text=datestr)
        self.pomodorolabel.config(text=pomodorostr)
        playlist = []
        if len(self.audiolist) != 0:
            for audio in range(len(self.audiolist)):
                playlist.append(str(audio) + " : " + os.path.basename(self.audiolist[int(audio)]))
            playlisttext = "\n".join(playlist)  # Join the playlist items with newlines
            self.playlistlabel.config(text=playlisttext)
        self.root.after(1000, self.updateclock)

#? END clock


def main():
    root = tk.Tk()
    app = RecluseBoard(root)
    root.mainloop()

if __name__ == "__main__":
    main()

#! SCHEDULE to do
#def table():
#    table=Tk()
#    dayFrame = Frame(table)
#    dayFrame.grid(row=0, column=0)
#    day = ["Day/Time","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
#    for x in range(25):
#        if(x==0):
#            daytxt = "Day\Time"#column0
#        else:
#            daytxt = "{0:0=2d}".format(x%24)+"00"
#        #Label(dayFrame, justify="center", text=daytxt, width=5,wraplength=80).grid(row=1, column=x, ipady=5, sticky='nesw')
#
#    tableFrame = Frame(table)
#    tableFrame.grid(row=1, column=0)
#    tabledata = readcsv('csv/week.csv')
#    for yaxis in range(8):
#        for xaxis in range(25):
#            day = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
#            if(yaxis==0):
#                if(xaxis==0):
#                    tableText = "Day\Time"#column0
#                else:
#                    tableText = "{0:0=2d}".format(xaxis%24)+"00"
#            else:
#                if(xaxis==0):
#                    tableText = day[yaxis-1]
#                else:
#                    tableText = tabledata[yaxis-1][xaxis-1]
#            bg = colorws
#            fg = colorb
#            Label(tableFrame, justify="center", text=tableText, bg=bg, fg=fg, wraplength=100).grid(row=yaxis, column=xaxis, ipady=5, sticky='nesw')
#    table.title("Schedule")
#    table.mainloop()
#
#######? END TABLE !######

#! icon with pillow
#        iconpath = self.geticonpath('./image/icon.png')
#        self.seticon(iconpath)
#
#    def geticonpath(self, filename):
#        """ Returns the absolute path to the icon file. """
#        if getattr(sys, 'frozen', False):
#            # If running in a frozen state (e.g., PyInstaller), use the bundled path
#            return os.path.join(sys._MEIPASS, filename)
#        else:
#            # Running in a development environment
#            return os.path.join(os.path.dirname(__file__), filename)
#
#    def seticon(self, iconpath):
#        """ Sets the window icon using Pillow. """
#        try:
#            icon = Image.open(iconpath)
#            self.root.iconphoto(True, ImageTk.PhotoImage(icon))
#        except Exception as e:
#            print(f"Error setting icon: {e}")

#! Luno price tracker
#        self.getlunoprice()
#        self.tracklunoprice()
#
#        self.lunourl = 'https://api.luno.com/api/1/ticker?pair=XRPMYR'
#
#    def getlunoprice(self):
#        try:
#            response = requests.get(self.lunorul)
#            data = response.json()
#            if 'last_trade' in data:
#                price = data['last_trade']
#                return price
#            else:
#                return None
#        except Exception as e:
#            print(f"Error fetching Luno price: {e}")
#            return None
#
#    def tracklunoprice(self,intervalseconds):
#        while True:
#            price = self.getlunoprice()
#            if price is not None:
#                print(f"Luno XRP/MYR Price: {price}")
#            else:
#                print("Unable to fetch Luno price.")
#            time.sleep(self.intervalseconds)
#
#    # Track Luno price every 60 seconds
#    self.tracklunoprice(self,60)