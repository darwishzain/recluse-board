import calendar,json,os,requests,socket,speedtest,sys,time,webbrowser
from datetime import timedelta
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit,QListWidget,QListWidgetItem, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

#print(socket.gethostbyname(socket.gethostname()))


def command(command):
    os.system(str(command))

class RecluseWindow(QMainWindow):
    def fullpath(self,relativepath:str)->str:
        directory = os.path.dirname(os.path.abspath(__file__))
        return(os.path.join(directory,relativepath))

    def openjson(self,filename):
        file = self.fullpath(filename)
        with open(file) as f:
            return(json.load(f))

    def editor(self,path):
        webbrowser.open(self.fullpath(path))

    def __init__(self):
        super().__init__()
        self.config = self.openjson(self.fullpath('config.json'))
        self.setWindowTitle(self.config['appname'])
        self.setWindowIcon(QIcon(self.fullpath("graphic/icon.ico")))
        self.setGeometry(100, 100, int(self.config['height']), int(self.config['width']))  # x, y, height, width
        font = self.config['fontfamily']
        fontsize = self.config['fontsize']
        self.fontsmall = QFont(font, int(fontsize['small']))
        self.fontmedium = QFont(font, int(fontsize['medium']))
        self.fontlarge = QFont(font, int(fontsize['large']))
        self.light = self.config['light']
        self.dark = self.config['dark']
        self.tomato = self.config['tomato']
        self.container = QWidget(self)
        self.setCentralWidget(self.container)
        self.container.setFont(self.fontsmall)

        self.layout = QVBoxLayout()
        self.container.setLayout(self.layout)


        #self.self = QGridLayout()  # row, column, span row, span column
        #self.container.setLayout(self.self)
        #self.container.setStyleSheet('background-color:' + self.config['background'] + ';color:' + self.config['foreground'])
        ##initui
        #welcome = QLabel("Welcome to Recluse Board", self.container)
        #welcome.setGeometry(0, 0, 300, 400)
        #self.self.addWidget(welcome, 0, 0, 1, 3)

        #* Clock, Date, Pomodoro
        self.time()

        self.middle = QHBoxLayout()
        self.layout.addLayout(self.middle)
        #* Buttons(Links,Projects,Commands,etc)
        self.buttons()
        #*Media Player
        self.mediaplayer()


        #* Update(1000ms)
        self.update()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def buttons(self):
        counter = 0
        buttonwidget = QWidget()
        buttonlayout = QGridLayout(buttonwidget)
        self.middle.addWidget(buttonwidget)
        self.data = self.openjson('data.json')
        links = self.data.get('link', {})
        commands = self.data.get('command', {})
        if links:
            for text,url in links.items():
                row = counter // 5
                column = counter % 5
                button =QPushButton(text,buttonwidget)
                button.clicked.connect(lambda checked,url=url:self.openurl(url))
                buttonlayout.addWidget(button,row,column)
                counter += 1
        if commands:
            for text,cmd in commands.items():
                row = counter // 5
                column = counter % 5
                button =QPushButton(text,buttonwidget)
                button.clicked.connect(lambda checked,cmd=cmd:self.runcommand(cmd))
                buttonlayout.addWidget(button,row,column)
                counter += 1

    def openurl(self, url):
        webbrowser.open(url)  # Open the URL in the browser

    def runcommand(self,cmd):
        os.system(str(cmd))

    def mediaplayer(self):
        self.mixer = mixer
        self.mixer.init()
        self.isplaying = False
        self.ispaused = True
        self.mediafile = None
        self.playindex = 0
        self.playlist = []
        mediawidget = QWidget()
        medialayout = QVBoxLayout(mediawidget)
        self.middle.addWidget(mediawidget)

        medialayout.addWidget(QLabel("Media Player"))
        self.mediatitle = QLabel("Player Empty")
        medialayout.addWidget(self.mediatitle)

        mediacontrol = QHBoxLayout()
        medialayout.addLayout(mediacontrol)
        #mediatitle = QVBoxLayout(mediawidget)
        #self.medialabel = QLabel("Media Player")
        #self.medialabel.setFixedWidth(200)
        #mediatitle.addWidget(self.medialabel, alignment=Qt.AlignmentFlag.AlignCenter)
        loadbtn = QPushButton()
        loadbtn.setIcon(QIcon(self.fullpath('graphic/load.png')))
        mediacontrol.addWidget(loadbtn)
#
        prevbtn = QPushButton()
        prevbtn.setIcon(QIcon(self.fullpath('graphic/previous.png')))
        mediacontrol.addWidget(prevbtn)

        self.playbtn = QPushButton()
        self.playbtn.setIcon(QIcon(self.fullpath('graphic/play.png'))) 
        mediacontrol.addWidget(self.playbtn)

        nextbtn = QPushButton()
        nextbtn.setIcon(QIcon(self.fullpath('graphic/next.png')))
        mediacontrol.addWidget(nextbtn)

        repebtn = QPushButton()#need to assign function soon
        repebtn.setIcon(QIcon(self.fullpath('graphic/repeat.png')))
        mediacontrol.addWidget(repebtn)

        # Connect media buttons to methods
        loadbtn.clicked.connect(self.loadmedia)
        prevbtn.clicked.connect(self.prevmedia)
        self.playbtn.clicked.connect(self.play)
        nextbtn.clicked.connect(self.nextmedia)

        self.mediaplaylist = QListWidget()
        medialayout.addWidget(self.mediaplaylist)

    def loadmedia(self):
        file = QFileDialog.getOpenFileName(self, 'Open File', '', 'Audio Files (*.mp3 *.wav *.ogg)')[0]
        if file:
            self.mediafile = file
            self.playlist.append({"title": os.path.basename(file), "path": file})
            self.mediaplaylist.clear()
            for index, media in enumerate(self.playlist):
                item = QListWidgetItem(media['title'])
                btn = QPushButton(media['title'])
                btn.clicked.connect(lambda checked, index=index: self.play(index))
                self.mediaplaylist.addItem(item)
                self.mediaplaylist.setItemWidget(item, btn)

    def play(self,index):
        if not self.playlist:
            self.mediatitle.setText("Playlist is empty! Nothing to play.")
            #print("Playlist is empty! Nothing to play.")
            self.playindex = None
            return
        if index is None:
            if self.playindex is None or self.playindex >= len(self.playlist):
                index = 0
            else:
                index = self.playindex

        # Clamp index within playlist bounds
        if index < 0 or index >= len(self.playlist):
            self.mediatitle.setText("Invalid index! Cannot play.")
            #print("Invalid index! Cannot play.")
            return
        media = self.playlist[index]
        self.playindex = index

        print(media['path'])
        self.mediatitle.setText(media['title'])
        self.mediatitle.setToolTip(media['title'])
        self.mixer.music.load(media['path'])
        self.mixer.music.play()

    def prevmedia(self):
        if not self.playlist:
            self.mediatitle.setText("Playlist is empty!")
            return
        self.playindex = (self.playindex - 1) % len(self.playlist)
        self.play(self.playindex)

    def nextmedia(self):
        if not self.playlist:
            self.mediatitle.setText("Playlist is empty!")
            return
        self.playindex = (self.playindex + 1) % len(self.playlist)
        self.play(self.playindex)

    def pomodoro(self,time):
        self.pomotime = time

    def time(self):
        self.pomotime = 0
        timewidget = QWidget()
        timelayout = QHBoxLayout(timewidget)
        self.layout.addWidget(timewidget)
        timewidget.setStyleSheet(self.tomato)

        clocklayout = QHBoxLayout()
        timelayout.addLayout(clocklayout)
        self.clock = QLabel("HH:MM:SS")
        self.clock.setFont(self.fontlarge)
        clocklayout.addWidget(self.clock)
        self.date = QLabel("DD/MM/YYYY")
        self.date.setFont(self.fontlarge)
        clocklayout.addWidget(self.date)

        pomolayout = QVBoxLayout()
        timelayout.addLayout(pomolayout)

        self.pomotimer = QLabel("HH:MM:SS")
        self.pomotimer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pomolayout.addWidget(self.pomotimer,stretch=1)
        self.pomotimer.setFont(self.fontlarge)
        pomocontrol = QHBoxLayout()
        pomolayout.addLayout(pomocontrol)
        self.pomo0 = QPushButton()
        self.pomo0.setIcon(QIcon(self.fullpath('graphic/refresh.png')))
        pomocontrol.addWidget(self.pomo0,stretch=0)
        self.pomo0.clicked.connect(lambda checked,time=0:self.pomodoro(time))
        self.pomo30 = QPushButton("+30")
        self.pomo30.clicked.connect(lambda checked,time=30:self.pomodoro(time))
        pomocontrol.addWidget(self.pomo30,stretch=0)

        pomoinput = QHBoxLayout()
        pomolayout.addLayout(pomoinput)
        self.pomoinput = QLineEdit()
        pomocontrol.addWidget(self.pomoinput,stretch=0)
        self.pomoinput.setStyleSheet('background-color:#F0F0F0;color:#000000;')
        self.pomocustom = QPushButton("+")
        self.pomocustom.clicked.connect(lambda checked:self.custompomo())
        pomocontrol.addWidget(self.pomocustom,stretch=0)

    def custompomo(self):
        self.pomodoro(int(self.pomoinput.text()))

    def update(self):
        clockstr = time.strftime('%H')+":"+time.strftime('%M')+":"+time.strftime('%S')
        datestr = time.strftime('%d')+"/"+time.strftime('%m')+"/"+time.strftime('%Y')
        if self.pomotime > 0:
            self.pomotime = self.pomotime - 1
        self.clock.setText(clockstr)
        self.date.setText(datestr)
        self.pomotimer.setText(str(timedelta(seconds=self.pomotime)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QPushButton {
            background-color: #F0F0F0;
            color: #000000;
            border-radius: 6px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #2E6DB4;
            color:#FFFFFF;
        }
        QPushButton:pressed {
            background-color: #E5533D;
        }
        QLineEdit{
            background-color:#F0F0F0;
            color:#FFFFFF;
        }
    """)

    window = RecluseWindow()
    window.show()
    sys.exit(app.exec())
