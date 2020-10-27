from flask import Flask
from main.database import engine
from pathlib import Path

UPLOAD_FOLDER = Path(__file__).parent / 'upload'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import main.views
