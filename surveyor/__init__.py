from flask import Flask
from flask.ext.pymongo import PyMongo

MONGO_DBNAME = "surveyor"
SECRET_KEY = "OMSIUOFYO(@#HUIbhlujhqf78oH*&@#FH"

app = Flask(__name__)
app.config.from_object(__name__)
mongo = PyMongo(app)

def get_survey(name):
    return mongo.db.surveys.find_one({"name": name})

import surveyor.views
