import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QListWidget, QListWidgetItem, QAbstractItemView,
    QHBoxLayout, QLabel, QPushButton,
)


class SongCard(QWidget):
    def __init__(self, title):
        super().__init__()

        layout = QHBoxLayout(self)

        label = QLabel(title)
        play_button = QPushButton("▶")
        info_button = QPushButton("Информация")

        layout.addWidget(label, 1)
        layout.addWidget(play_button)
        layout.addWidget(info_button)

        play_button.clicked.connect(
            lambda checked: print("Воспроизвести:", title)
        )
        info_button.clicked.connect(
            lambda checked: print("Информация:", title)
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 350)

        self.song_list = QListWidget()
        self.song_list.setDragDropMode(
            QAbstractItemView.DragDropMode.InternalMove
        )
        self.song_list.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.setCentralWidget(self.song_list)

        for title in ["Песня 1", "Песня 2", "Песня 3"]:
            self.add_song(title)

    def add_song(self, title):
        card = SongCard(title)

        item = QListWidgetItem()
        item.setSizeHint(card.sizeHint())

        # Перемещаем между строками, а не вкладываем одну в другую.
        item.setFlags(
            item.flags() & ~Qt.ItemFlag.ItemIsDropEnabled
        )

        self.song_list.addItem(item)
        self.song_list.setItemWidget(item, card)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())