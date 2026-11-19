# Karaoke App build by EESTEC Aachen

To start the app, you need to have Node.js installed on your machine. You can download it from [Node.js official website](https://nodejs.org/).
You also need Python installed on your machine. You can download it from [Python official website](https://www.python.org/).


Download the dependencies by running:
```
python -m pip install -r requirements.txt
```

To build the frontend, run: (This step is optional, if no frontend is built a legacy html file is served by default)
```
python build_frontend.py
```

To start the server, run:
```
python main.py
```
The server will be accessible at `http://localhost:8000` in your web browser (guest request page at `/qr`).

To start the PyQt desktop control panel (it also starts the server in the background), run:
```
python desktop/main.py
```