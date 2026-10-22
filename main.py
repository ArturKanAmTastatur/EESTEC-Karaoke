import ctypes
import sys
from ctypes import wintypes

from PyQt6.QtCore import Qt

from youtubeInteraction import *
from exceptions import *

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QWidget, QAbstractItemView, QListWidgetItem, QDialog
)
from PyQt6.QtCore import pyqtSignal
import os


def verification(input_password):
    if (input_password == password):
        return True
    else:
        return False


class SongCard(QWidget):
    song_delete_sygnal = pyqtSignal(object)

    def __init__(self, url, title="", customer=""):
        super().__init__()
        uic.loadUi("songcard.ui", self)
        self.stackedWidget.setCurrentIndex(0)

        self.url = url
        self.cardInfo = title + ("" if customer == "" else (" for " + customer))

        self.labelTitle.setText(self.cardInfo)
        self.labelTitleEdit.setText(self.cardInfo)

        self.deleteButton.clicked.connect(self.delete_song)

    def delete_song(self):
        self.song_delete_sygnal.emit(self)


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
        self.dialSound.setValue(50)

        self.currentSong = None
        self.editMode = False

        self.songList.setDragDropMode(
            QAbstractItemView.DragDropMode.NoDragDrop
        )
        self.songList.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.editURL.returnPressed.connect(self.editTitle.setFocus)
        self.editTitle.returnPressed.connect(self.editCustomer.setFocus)
        self.editCustomer.returnPressed.connect(self.add_song)

        self.addButton.clicked.connect(self.add_song)
        self.playButton.clicked.connect(self.play_stop)
        self.nextButton.clicked.connect(self.next_song)
        self.editModeButton.clicked.connect(self.edit_mode_check)

        self.songList.model().rowsMoved.connect(self.check_current_song_changed)
        self.dialSound.valueChanged.connect(self.change_sound_volume)

    def edit_mode_check(self):
        try:
            if (self.editMode == True):

                self.editMode = False
                self.songList.setDragDropMode(
                    QAbstractItemView.DragDropMode.NoDragDrop
                )
                for i in range(self.songList.count()):
                    item = self.songList.itemWidget(self.songList.item(i))
                    item.stackedWidget.setCurrentIndex(0)
            else:
                password_check = PasswordDialogue()
                if password_check.exec():

                    self.editMode = True
                    self.songList.setDragDropMode(
                        QAbstractItemView.DragDropMode.InternalMove
                    )
                    for i in range(self.songList.count()):
                        item = self.songList.itemWidget(self.songList.item(i))
                        item.stackedWidget.setCurrentIndex(1)
                else:
                    return
        except Exception as e:
            print(e)

    def change_sound_volume(self, value):
        try:
            self.command_signal.emit(2, str(value))
        except Exception as e:
            print(e)

    def play_stop(self, checked):
        try:
            if self.currentSong is None:
                self.playButton.setText("Play ▶")
                raise EmptyQueueException
            if checked:
                self.playButton.setText("Stop ⏸")
                self.command_signal.emit(1, "")
            else:
                self.playButton.setText("Play ▶")
                self.command_signal.emit(0, "")
        except EmptyQueueException:
            self.labelError.setText("No songs to play")
            self.playButton.setChecked(False)

    def next_song(self):
        try:
            currentSong = self.songList.itemWidget(self.songList.item(0))
            if (currentSong == None):
                self.labelError.setText("No song to play")
                return
            password_check = PasswordDialogue()
            if password_check.exec():
                self.songList.takeItem(0)
                currentSong = self.songList.itemWidget(self.songList.item(0))
                if (currentSong == None):
                    self.command_signal.emit(3, "")
                else:
                    self.check_current_song_changed()
            else:
                return
        except Exception as e:
            print(e)

    def add_song(self):
        url = self.editURL.text()
        title = self.editTitle.text()
        customer = self.editCustomer.text()

        try:
            if (url == ""):
                raise AbsentURLException
            else:
                youtube_video_exists(url)
            if (title == ""):
                title = get_youtube_title(url)

            self.labelError.setText("")

            songCard = SongCard(url, title, customer)
            songCard.song_delete_sygnal.connect(self.delete_song)

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

            self.check_current_song_changed()

        except AbsentURLException:
            self.labelError.setText("URL cannot be empty")
        except InvalidURLException:
            self.labelError.setText("URL is invalid or video is private.")
        except Exception as e:
            print(e)

    def delete_song(self, card):
        for i in range(self.songList.count()):
            if self.songList.itemWidget(self.songList.item(i)) is card:
                self.songList.takeItem(i)
                card.deleteLater()
            self.check_current_song_changed()


    def check_current_song_changed(self):
        currentSong = self.songList.itemWidget(self.songList.item(0))
        try:
            if (currentSong is None):
                self.currentSongLabel.setText("")
                self.playButton.setChecked(False)
                self.playButton.setText("Play ▶")
                self.command_signal.emit(3, "")
                return
            if (self.currentSong != currentSong):
                self.currentSong = currentSong
                self.play_song(get_youtube_video_id(self.currentSong.url), self.currentSong.cardInfo)
        except Exception as e:
            print(e)

    def play_song(self, id, info):
        try:
            if not self.playButton.isChecked():
                self.playButton.setChecked(True)
                self.play_stop(True)

            self.currentSongLabel.setText(info)
            self.song_signal.emit(id)
        except Exception as e:
            print(e)


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
        if signal == 2:
            self.displayWidget.set_volume(aux)
        if signal == 3:
            self.displayWidget.clear()

    def play_song(self, id):
        try:
            self.displayWidget.play_video(id)
        except Exception as e:
            print(e)

    def keyPressEvent(self, event):
        print(event.key())
        if (event.key() == Qt.Key.Key_F11):
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()
        else:
            super().keyPressEvent(event)

class PasswordDialogue(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("password.ui", self)

        self.submitButton.clicked.connect(self.check_password)
        self.cancelButton.clicked.connect(self.close)

    def check_password(self):
        response = verification(self.inputLine.text())
        if (response):
            self.accept()
        else:
            self.errorLabel.setText("Wrong password")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    control_panel = KaraokeMain()
    display = KaraokeDisplay()

    password = os.environ.get("PASSWORD")

    control_panel.command_signal.connect(display.signal_receiver)
    control_panel.song_signal.connect(display.play_song)

    display.displayWidget.set_volume(control_panel.dialSound.value())
    display.displayWidget.video_ended.connect(control_panel.next_song)

    control_panel.show()
    display.show()
    app.exec()