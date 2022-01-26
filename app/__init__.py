from pathlib import Path

from flask import Flask
from app import config


def create_app(*args, **kwargs):
    app = Flask(__name__)
    app.debug = True
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.config['BASEDIR'] = Path(__file__).parent.parent
    app.secret_key = 'ppdf'
    app.config['SESSION_TYPE'] = 'filesystem'

    return app
