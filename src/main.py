import calendar,json,os,requests,socket,speedtest,sys,time,webbrowser
from datetime import timedelta
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from PyQt6.QtCore import QTimer, QSize
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QListWidget, QMainWindow, QPushButton, QVBoxLayout, QWidget

print(socket.gethostbyname(socket.gethostname()))


def command(command):
    os.system(str(command))

class RecluseWindow(QMainWindow):
    def fullpath(self,relativepath):
        directory = os.path.dirname(__file__)
        return(os.path.join(directory,relativepath))

    def openjson(self,filename):
        file = self.fullpath(filename)
        with open(file) as f:
            jsondata = json.load(f)
        return(jsondata)

    def editor(self,filedirectory):
        webbrowser.open(self.fullpath(filedirectory))

    def __init__(self):
        super().__init__()
        self.config = self.openjson(self.fullpath('config.json'))
        self.setWindowTitle(self.config['appname'])
        self.setWindowIcon(QIcon(self.fullpath("graphic/icon.ico")))
        self.setGeometry(100, 100, int(self.config['height']), int(self.config['width']))  # x, y, height, width
        self.fontsmall = QFont(self.config['fontfamily'], int(self.config['fontsize']['small']))
        self.fontmedium = QFont(self.config['fontfamily'], int(self.config['fontsize']['medium']))
        self.fontlarge = QFont(self.config['fontfamily'], int(self.config['fontsize']['large']))

        self.container = QWidget(self)
        self.container.setFont(self.fontsmall)
        self.setCentralWidget(self.container)

        self.self = QGridLayout()  # row, column, span row, span column
        self.container.setLayout(self.self)
        self.container.setStyleSheet('background-color:' + self.config['background'] + ';color:' + self.config['foreground'])
        #initui
        welcome = QLabel("Welcome to Recluse Board", self.container)
        welcome.setGeometry(0, 0, 300, 400)
        self.self.addWidget(welcome, 0, 0, 1, 3)

        #* Buttons(Links,Projects,Commands,etc)
        self.buttons()
        #*Media Player
        self.mediaplayer()
        #* Clock, Date, Pomodoro
        self.clock()

        #* Update(1000ms)
        self.update()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def buttons(self):
        buttonwidget = QWidget(self.container)
        buttonlayout = QGridLayout(buttonwidget)  # Set layout for button widget
        self.self.addWidget(buttonwidget, 2, 0)
        counter = 0
        # Assuming openjson('./data.json')['link'] returns a dictionary of text and url
        for text, url in self.openjson('./data.json')['link'].items():
            row = counter // 5
            column = counter % 5
            button = QPushButton(text, buttonwidget)
            button.clicked.connect(lambda checked, url=url: self.open_url(url))  # Connect button to URL
            buttonlayout.addWidget(button, row, column)
            counter += 1

    def open_url(self, url):
        webbrowser.open(url)  # Open the URL in the browser

    def mediaplayer(self):
        self.mixer = mixer
        self.mixer.init()
        self.isplaying = False
        self.ispaused = True
        self.mediafile = None
        mediawidget = QWidget(self.container)
        self.self.addWidget(mediawidget, 1, 1)
        
        mediatitle = QVBoxLayout(mediawidget)
        self.medialabel = QLabel("Media Player")
        mediatitle.addWidget(self.medialabel)

        mediacontrol = QHBoxLayout()
        mediatitle.addLayout(mediacontrol)

        loadbtn = QPushButton()
        loadbtn.setIcon(QIcon(self.fullpath('graphic/load.png')))
        mediacontrol.addWidget(loadbtn)

        prevbtn = QPushButton()
        prevbtn.setIcon(QIcon(self.fullpath('graphic/previous.png')))
        mediacontrol.addWidget(prevbtn)

        self.playbtn = QPushButton()
        self.playbtn.setIcon(QIcon(self.fullpath('graphic/play.png'))) 
        mediacontrol.addWidget(self.playbtn)

        nextbtn = QPushButton()
        nextbtn.setIcon(QIcon(self.fullpath('graphic/next.png')))
        mediacontrol.addWidget(nextbtn)

        repebtn = QPushButton()
        repebtn.setIcon(QIcon(self.fullpath('graphic/next.png')))
        mediacontrol.addWidget(repebtn)

        # Connect media buttons to methods
        loadbtn.clicked.connect(self.loadmedia)
        prevbtn.clicked.connect(self.prevmedia)
        self.playbtn.clicked.connect(self.playmedia)
        nextbtn.clicked.connect(self.nextmedia)
        
        self.playlist = QListWidget()
        mediatitle.addWidget(self.playlist)

    def loadmedia(self):
        file = QFileDialog.getOpenFileName(self, 'Open File', '', 'Audio Files (*.mp3 *.wav *.ogg *.m4a *.flac *.aac *.opus *.aiff *.wma)')[0]
        if file:
            self.mediafile = file
            self.playlist.addItem(file)
            #self.medialabel.setText(os.path.basename(file))

    def mediaplaylist(self):
        print(self.mediaplaylist)

    def playmedia(self):
        item = self.playlist.currentItem()
        if item is None and self.playlist.count() > 0:
            item = self.playlist.item(0)
            self.playlist.setCurrentItem(item)
        if item:
            path = item.text()
            self.medialabel.setText(os.path.basename(path))
            self.mixer.music.load(path)
            self.mixer.music.play()
    
    def prevmedia(self):
        count = self.playlist.count()
        if count == 0:
            return
        current_row = self.playlist.currentRow()
        prev_row = (current_row - 1 + count) % count  # 🔁 loop back to last
        self.playlist.setCurrentRow(prev_row)
        self.playmedia()

    def nextmedia(self):
        count = self.playlist.count()
        if count == 0:
            return
        current_row = self.playlist.currentRow()
        next_row = (current_row + 1) % count  # 🔁 loop back to 0
        self.playlist.setCurrentRow(next_row)
        self.playmedia()


    def clock(self):
        timewidget = QWidget(self.container)
        timelayout = QHBoxLayout(timewidget)
        self.self.addWidget(timewidget,1,0)
        self.pomotime = 0
        self.clock = QLabel("HH:MM:SS")
        timelayout.addWidget(self.clock)
        self.date = QLabel("DD/MM/YY")
        timelayout.addWidget(self.date)
        self.pomo = QLabel("HH:MM:SS")
        timelayout.addWidget(self.pomo)

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
