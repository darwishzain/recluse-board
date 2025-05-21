import calendar
from datetime import timedelta
import json
import os
import requests
import sys
import time
import webbrowser
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QFileDialog, QGridLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

def fullpath(relativepath):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, relativepath)

def openjson(filename):
    file = fullpath(filename)
    with open(file) as f:
        jsondata = json.load(f)
    return jsondata

def editor(filedirectory):
    webbrowser.open(fullpath(filedirectory))

def command(command):
    os.system(str(command))

config = openjson(fullpath('config.json'))

class RecluseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config['appname'])
        self.setGeometry(100, 100, int(config['height']), int(config['width']))  # x, y, height, width
        self.fontsmall = QFont(config['fontfamily'], int(config['fontsize']['small']))
        self.fontmedium = QFont(config['fontfamily'], int(config['fontsize']['medium']))
        self.fontlarge = QFont(config['fontfamily'], int(config['fontsize']['large']))

        self.container = QWidget(self)
        self.container.setFont(self.fontsmall)
        self.setCentralWidget(self.container)

        self.grid = QGridLayout()  # row, column, span row, span column
        self.container.setLayout(self.grid)
        self.container.setStyleSheet('background-color:' + config['background'] + ';color:' + config['foreground'])

        self.init_ui()
        #* Buttons(Links,Projects,Commands,etc)
        self.buttons()
        #*Media Player
        self.mediaplayer()
        self.mixer = mixer
        self.mixer.init()
        self.isplaying = False
        self.ispaused = True
        self.mediafile = None
        #* Clock, Date, Pomodoro
        self.clock()

        #* Update(1000ms)
        self.update()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def init_ui(self):
        self.welcome = QLabel("Welcome to Recluse Board", self.container)
        self.welcome.setGeometry(0, 0, 300, 400)
        self.grid.addWidget(self.welcome, 0, 0, 1, 3)

        # Set up button widget and media widget
        self.buttonwidget = QWidget(self.container)
        self.buttonlayout = QGridLayout(self.buttonwidget)  # Set layout for button widget
        self.grid.addWidget(self.buttonwidget, 2, 0)

        self.mediawidget = QWidget(self.container)
        self.grid.addWidget(self.mediawidget, 2, 1)
        self.medialayout = QVBoxLayout(self.mediawidget)

        self.timewidget = QWidget(self.container)
        self.timelayout = QGridLayout(self.timewidget)
        self.grid.addWidget(self.timewidget,1,0)

    def buttons(self):
        counter = 0
        # Assuming openjson('./data.json')['link'] returns a dictionary of text and url
        for text, url in openjson('./data.json')['link'].items():
            row = counter // 5
            column = counter % 5
            self.button = QPushButton(text, self.buttonwidget)
            self.button.clicked.connect(lambda checked, url=url: self.open_url(url))  # Connect button to URL
            self.buttonlayout.addWidget(self.button, row, column)
            counter += 1

    def open_url(self, url):
        webbrowser.open(url)  # Open the URL in the browser

    def mediaplayer(self):
        self.medialabel = QLabel("Media Player", self.mediawidget)
        self.medialayout.addWidget(self.medialabel)

        self.loadbtn = QPushButton("Load", self.mediawidget)
        self.medialayout.addWidget(self.loadbtn)

        self.prevbtn = QPushButton("Prev", self.mediawidget)
        self.medialayout.addWidget(self.prevbtn)

        self.playbtn = QPushButton("Play", self.mediawidget)
        self.medialayout.addWidget(self.playbtn)

        self.nextbtn = QPushButton("Next", self.mediawidget)  # Fixed redundancy
        self.medialayout.addWidget(self.nextbtn)

        # Connect media buttons to methods
        self.loadbtn.clicked.connect(self.loadmedia)
        self.prevbtn.clicked.connect(self.prevmedia)
        self.playbtn.clicked.connect(self.playmedia)
        self.nextbtn.clicked.connect(self.nextmedia)

    def loadmedia(self):
        file = QFileDialog.getOpenFileName(self, 'Open File', '', 'Audio Files (*.mp3 *.wav *.ogg)')[0]
        if file:
            self.mediafile = file
            self.mixer.music.load(self.mediafile)
            self.medialabel.setText(os.path.basename(file))

    def mediaplaylist(self):
        print(self.mediaplaylist)
    def prevmedia(self):
        print("Previous media")

    def playmedia(self):
        if self.mediafile:
            print("Playing media")

    def nextmedia(self):
        print("Next media")

    def clock(self):
        self.pomotime = 0
        self.clock = QLabel("HH:MM:SS")
        self.timelayout.addWidget(self.clock)
        self.date = QLabel("DD/MM/YY")
        self.timelayout.addWidget(self.date)
        self.pomo = QLabel("HH:MM:SS")
        self.timelayout.addWidget(self.pomo)

    def update(self):
        clockstr = time.strftime('%H')+":"+time.strftime('%M')+":"+time.strftime('%S')
        datestr = time.strftime('%d')+"/"+time.strftime('%m')+"/"+time.strftime('%Y')
        if self.pomotime > 0:
            self.pomotime = self.pomotime - 1
        self.clock.setText(clockstr)
        self.date.setText(datestr)
        self.pomo.setText(str(timedelta(seconds=self.pomotime)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecluseWindow()
    window.show()
    sys.exit(app.exec())
