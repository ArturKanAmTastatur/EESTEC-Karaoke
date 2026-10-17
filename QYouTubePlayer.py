import json

from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class QYouTubePlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(
            QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.web_view)

    def play_video(self, video_id, muted=False):
        html = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0; background:black; overflow:hidden;">
          <iframe id="player"
                  src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute={int(muted)}&enablejsapi=1"
                  style="border:0; width:100vw; height:100vh;"
                  referrerpolicy="strict-origin-when-cross-origin"
                  allow="autoplay; encrypted-media; fullscreen"
                  allowfullscreen></iframe>
        </body>
        </html>
        """
        self.web_view.setHtml(html, QUrl("https://localhost/"))

    def command(self, func, *args):
        msg = json.dumps({"event": "command", "func": func, "args": list(args)})
        self.web_view.page().runJavaScript(
            f"document.getElementById('player').contentWindow.postMessage({msg!r}, '*');"
        )