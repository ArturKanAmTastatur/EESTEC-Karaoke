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

To start the application, run:
```
python main.py
```
This starts the pyQt application and the backend server. The application will be accessible at `http://localhost:8000` in your web browser.