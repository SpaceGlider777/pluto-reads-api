from flask import Flask
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app, resources={"*": {"origins": "http://localhost:4200"}})
model = joblib.load('model.pkl')

from app import routes