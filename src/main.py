import calendar
import json
import os
import requests
import sys
import time
import webbrowser
from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
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

        self.container = QWidget(self)
        self.setCentralWidget(self.container)
        self.grid = QGridLayout()  # row, column, span row, span column
        self.container.setLayout(self.grid)
        self.container.setStyleSheet('background-color:' + config['background'] + ';color:' + config['foreground'])

        self.init_ui()
        self.buttons()
        self.mediaplayer()

    def init_ui(self):
        self.welcome = QLabel("Welcome to Recluse Board", self.container)
        self.welcome.setGeometry(0, 0, 300, 400)
        self.grid.addWidget(self.welcome, 0, 0, 1, 3)

        # Set up button widget and media widget
        self.buttonwidget = QWidget(self.container)
        self.buttonlayout = QGridLayout(self.buttonwidget)  # Set layout for button widget
        self.grid.addWidget(self.buttonwidget, 1, 0)

        self.mediawidget = QWidget(self.container)
        self.grid.addWidget(self.mediawidget, 1, 1)
        self.medialayout = QVBoxLayout(self.mediawidget)

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
        self.loadbtn.clicked.connect(self.load_media)
        self.prevbtn.clicked.connect(self.prev_media)
        self.playbtn.clicked.connect(self.play_media)
        self.nextbtn.clicked.connect(self.next_media)

    def load_media(self):
        print("Load media")

    def prev_media(self):
        print("Previous media")

    def play_media(self):
        print("Play media")

    def next_media(self):
        print("Next media")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecluseWindow()
    window.show()
    sys.exit(app.exec())
