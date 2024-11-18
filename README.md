# Recluse Board
[![Download Recluse Board](https://img.shields.io/sourceforge/dm/recluseboard.svg)](https://sourceforge.net/projects/recluseboard/files/latest/download) ![GitHub Sponsors](https://img.shields.io/github/sponsors/darwishzain)

![](https://img.shields.io/badge/Code-Python3.11.x-informational?style=flat&logo=python&logoColor=white&color=2bbc8a) ![](https://img.shields.io/badge/Tools-Tkinter-informational?style=flat&logoColor=white) ![](https://img.shields.io/badge/Tools-Pygame-informational?style=flat&logoColor=white) ![](https://img.shields.io/badge/Tools-CSV-informational?style=flat&logoColor=white)

### Interface
![](images/interface.png)

![](images/table.png)

## Installation

```console
# clone the repo
$ git clone https://github.com/darwishzain/recluse-board.git

# change the working directory to recluse-board
$ cd recluse-board

# install the requirements
$ python3 -m pip install -r requirements.txt
```

## Run Recluse Board
```
# Run Recluse Board from Command Line
$ cd src
$ python -u main.py
```

## Development
### Debian
#### Install python virtual environment
```
sudo apt-get install python3-venv
```
#### Activate virtual environment
```
source myenv/bin/activate  # On Linux/macOS
myenv\Scripts\activate  # On Windows
```

## Syntax

#### link.csv
```
name,link
name,link
```
Example
```
Github,https://github.com
Facebook,https://facebook.com
```
Result
![](images/linkcsv.png)

#### week.csv

```
activity,activity,activity,activity,activity
```
Example
```
Sleep,Study,Exercise,Reading,Cooking
```

### Default CSV
#### link.csv
```
Example Google, https://google.com
Example Youtube,https://studio.youtube.com/
Example Github,https://github.com
Example Sci-Hub,https://sci-hub.se/
Example OneDrive,https://onedrive.live.com/
"Jeli.my",https://jeli.com.my/index.php?home
```
#### shortcut.csv
```
Users File,C:\Users
C,C:\
CSV,./csv
VLC,C:\Program Files (x86)\VideoLAN\VLC\vlc.exe
```
Result
![](images/weekcsv.png)

#### Stargazer
[![Stargazers repo roster for @darwishzain/recluse-board](https://reporoster.com/stars/dark/darwishzain/recluse-board)](https://github.com/darwishzain/recluse-board/stargazers)
