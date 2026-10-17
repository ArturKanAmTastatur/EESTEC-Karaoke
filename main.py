import io
import re
import sys

from PyQt6.QtCore import Qt, QUrl

from QYouTubePlayer import QYouTubePlayer
from youtubeInteraction import *
from exceptions import *

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QWidget, QAbstractItemView, QListWidgetItem
)
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView




class SongCard(QWidget):
    def __init__(self, url, title, customer):
        super().__init__()
        uic.loadUi("songcard.ui", self)
        self.stackedWidget.setCurrentIndex(0)

        self.url = url
        self.cardInfo = title + ("" if customer == "" else (" for " + customer))

        self.labelTitle.setText(self.cardInfo)


class KaraokeMain(QMainWindow):
    song_signal = pyqtSignal(str)  # song
    command_signal = pyqtSignal(int, str)  # signal type, additional info

    def __init__(self):
        super().__init__()
        uic.loadUi("control_panel.ui", self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("EESTEC Karaoke Control Panel")
        self.setFixedSize(1090, 740)

        self.labelError.setText("")
        self.playButton.setChecked(False)
        self.displayWidget.command("setVolume", 0)

        self.currentSong = None

        self.songList.setDragDropMode(
            QAbstractItemView.DragDropMode.InternalMove
        )
        self.songList.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.addButton.clicked.connect(self.add_song)
        self.playButton.clicked.connect(self.play_stop)
        self.songList.model().rowsMoved.connect(self.check_current_song)

    def play_stop(self, checked):
        try:
            if checked:
                self.playButton.setText("Stop ⏸")
                self.displayWidget.command("playVideo")
                self.command_signal.emit(1, "")
            else:
                self.playButton.setText("Play ▶")
                self.displayWidget.command("pauseVideo")
                self.command_signal.emit(0, "")
        except Exception as e:
            print(e)

    def play_song(self, id):
        try:
            if not self.playButton.isChecked():
                self.playButton.setChecked(True)
                self.play_stop(True)

            self.displayWidget.play_video(id, True)
            self.song_signal.emit(id)
        except Exception as e:
            print(e)

    def next_song(self):
        self.songList.takeItem(0)
        self.check_current_song()

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

            self.check_current_song()

        except AbsentURLException:
            self.labelError.setText("URL cannot be empty")
        except InvalidURLException:
            self.labelError.setText("URL is invalid or video is private.")
        except Exception as e:
            print(e)

    def check_current_song(self):
        curentSong = self.songList.itemWidget(self.songList.item(0))
        if (self.currentSong != curentSong):
            self.currentSong = curentSong
            self.play_song(get_youtube_video_id(self.currentSong.url))


class KaraokeDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("display.ui", self)

        self.setWindowTitle("EESTEC Karaoke Display")

    def play_stop(self, checked):
        try:
            if checked == 1:
                self.displayWidget.command("playVideo")
            else:
                self.displayWidget.command("pauseVideo")
        except Exception as e:
            print(e)

    def signal_receiver(self, signal, aux):
        if signal in [0, 1]:
            self.play_stop(signal)

    def play_song(self, id):
        try:
            self.displayWidget.play_video(id)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    control_panel = KaraokeMain()
    display = KaraokeDisplay()

    control_panel.command_signal.connect(display.signal_receiver)
    control_panel.song_signal.connect(display.play_song)

    display.displayWidget.video_ended.connect(control_panel.next_song)

    control_panel.show()
    display.show()
    app.exec()