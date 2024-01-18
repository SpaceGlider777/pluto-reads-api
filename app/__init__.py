from flask import Flask
from flask_cors import CORS
import pandas
import joblib

app = Flask(__name__)
CORS(app, resources={"*": {"origins": "http://localhost:4200"}})
model = joblib.load('model.pkl')
books = pandas.read_pickle('books')
ratings = pandas.read_pickle('ratings')
matrix = pandas.read_pickle('matrix')

from app import routes