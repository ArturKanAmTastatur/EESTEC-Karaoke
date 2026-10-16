import io
import sys

from PyQt6.QtCore import Qt

import exceptions
import requests

from exceptions import AbsentURLException

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QWidget, QAbstractItemView, QListWidgetItem
)
from PyQt6.QtCore import QObject, pyqtSignal

def youtube_video_exists(url):
    r = requests.get(
        "https://www.youtube.com/oembed",
        params={"url": url, "format": "json"},
        timeout=5,
    )
    if (r.status_code == 200):
        return True
    else:
        raise exceptions.InvalidURLException()

def get_youtube_title(url):
    check = youtube_video_exists(url)
    r = requests.get(
        "https://www.youtube.com/oembed",
        params={"url": url, "format": "json"},
        timeout=5,
    )
    if r.status_code == 200:
        return r.json()["title"]


class SongCard(QWidget):
    def __init__(self, url, title, customer):
        super().__init__()
        uic.loadUi("songcard.ui", self)
        self.stackedWidget.setCurrentIndex(0)
        self.url = url
        self.cardInfo = title + ("" if customer == "" else (" for " + customer))
        print(customer, self.cardInfo)
        self.labelTitle.setText(self.cardInfo)

class KaraokeMain(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("template.ui", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("EESTEC Karaoke")
        self.setFixedSize(1090, 740)

        self.labelError.setText("")
        self.playButton.setChecked(False)

        self.songList.setDragDropMode(
            QAbstractItemView.DragDropMode.InternalMove
        )
        self.songList.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.addButton.clicked.connect(self.add_song)
        self.playButton.clicked.connect(self.play_song)

    def play_song(self, checked):
        try:
            if checked:
                self.playButton.setText("Stop ⏸")
            else:
                self.playButton.setText("Play ▶")
        except Exception as e:
            print(e)

    def add_song(self):
        url = self.editURL.text()
        title = self.editTitle.text()
        customer = self.editCustomer.text()

        try:
            if (url == ""):
                raise AbsentURLException
            if (title == ""):
                title = get_youtube_title(url)

            self.labelError.setText("")

            songCard = SongCard(url, title, customer)
            item = QListWidgetItem()
            item.setSizeHint(songCard.sizeHint())

            item.setFlags(
                item.flags() & ~Qt.ItemFlag.ItemIsDropEnabled
            )

            self.songList.addItem(item)
            self.songList.setItemWidget(item, songCard)

            self.editURL.setText("")
            self.editTitle.setText("")
            self.editCustomer.setText("")

        except AbsentURLException:
            self.labelError.setText("URL cannot be empty")
        except exceptions.InvalidURLException:
            self.labelError.setText("URL is invalid or video is private.")
        except Exception as e:
            print(e)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KaraokeMain()
    window.show()
    app.exec()