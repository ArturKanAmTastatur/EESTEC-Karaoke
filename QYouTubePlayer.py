import json

from PyQt6.QtCore import QUrl, pyqtSignal
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class QYouTubePlayer(QWidget):
    state_changed = pyqtSignal(int)   # любое изменение состояния
    video_ended = pyqtSignal()        # видео закончилось

    def __init__(self, parent=None):
        super().__init__(parent)
        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(
            QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False
        )

        self.volume = 50

        self.web_view.titleChanged.connect(self._on_title_changed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.web_view)

    def play_video(self, video_id, muted=False):
        html = f"""
            <style>
              body {{ margin:0; background:black; }}
              #player {{ position:fixed; width:100%; height:100%; pointer-events:none; }}
            </style>
            <div id="player"></div>
            <script src="https://www.youtube.com/iframe_api"></script>
            <script>
              var player;
              function onYouTubeIframeAPIReady() {{
                player = new YT.Player('player', {{
                  videoId: '{video_id}',
                  playerVars: {{ autoplay: {1},
                    mute: {int(muted)} }},
                  events: {{ 
                    onReady: e => {{e.target.setVolume({self.volume}); e.target.playVideo(); }}
                    onStateChange: e => document.title = 'state:' + e.data }}
                }});
              }}
            </script>
            """
        self.web_view.setHtml(html, QUrl("https://localhost/"))

    def set_volume(self, value):
        self.volume = int(value)
        self.command("setVolume", self.volume)

    def command(self, func, *args):
        allowed_funcs = ["setVolume", "playVideo", "pauseVideo", "stopVideo", "seekTo", "setPlaybackRate", "setLoop", "setShuffle"]
        if func not in allowed_funcs:
            return
        js_args = ", ".join(json.dumps(a) for a in args)
        self.web_view.page().runJavaScript(
            f"if (window.player && player.{func}) player.{func}({js_args});"
        )

    def _on_title_changed(self, title):
        if title.startswith("state:"):
            state = int(title[len("state:"):])
            self.state_changed.emit(state)
            if state == 0:
                self.video_ended.emit()

    def clear(self):
        self.web_view.setHtml("<body style='margin:0; background:black'></body>")