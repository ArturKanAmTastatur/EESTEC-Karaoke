import sys
import ctypes
from ctypes import wintypes

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

DWMWA_WINDOW_CORNER_PREFERENCE = 33
DWMWCP_DEFAULT = 0
DWMWCP_DONOTROUND = 1

DWMWA_BORDER_COLOR = 34
DWMWA_COLOR_DEFAULT = 0xFFFFFFFF
DWMWA_COLOR_NONE = 0xFFFFFFFE


def set_dwm_frame(widget, fullscreen):
    if sys.platform != "win32":
        return
    try:
        dwm = ctypes.windll.dwmapi
    except (AttributeError, OSError):
        return

    hwnd = wintypes.HWND(int(widget.winId()))

    corner = ctypes.c_int(DWMWCP_DONOTROUND if fullscreen else DWMWCP_DEFAULT)
    dwm.DwmSetWindowAttribute(
        hwnd, DWMWA_WINDOW_CORNER_PREFERENCE,
        ctypes.byref(corner), ctypes.sizeof(corner),
    )

    color = ctypes.c_uint(DWMWA_COLOR_NONE if fullscreen else DWMWA_COLOR_DEFAULT)
    dwm.DwmSetWindowAttribute(
        hwnd, DWMWA_BORDER_COLOR,
        ctypes.byref(color), ctypes.sizeof(color),
    )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 fullscreen без рамки")
        self.resize(800, 500)

        central = QWidget()
        central.setStyleSheet("background-color: #202830;")
        layout = QVBoxLayout(central)
        label = QLabel("F11 — полноэкранный режим\nEsc — выход")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white; font-size: 24px;")
        layout.addWidget(label)
        self.setCentralWidget(central)

        QShortcut(QKeySequence("F11"), self, activated=self.toggle_fullscreen)
        QShortcut(QKeySequence("Esc"), self, activated=self.close)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def showEvent(self, event):
        super().showEvent(event)
        set_dwm_frame(self, self.isFullScreen())

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.Type.WindowStateChange:
            set_dwm_frame(self, self.isFullScreen())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())