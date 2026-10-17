import json
import re

import requests
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from exceptions import *


def youtube_video_exists(url):
    r = requests.get(
        "https://www.youtube.com/oembed",
        params={"url": url, "format": "json"},
        timeout=5,
    )
    if (r.status_code == 200):
        return True
    else:
        raise InvalidURLException()

def get_youtube_title(url):
    r = requests.get(
        "https://www.youtube.com/oembed",
        params={"url": url, "format": "json"},
        timeout=5,
    )
    if r.status_code == 200:
        return r.json()["title"]

def get_youtube_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([\w-]{11})", url)
    if match:
        return match.group(1)
    else:
        raise InvalidURLException()