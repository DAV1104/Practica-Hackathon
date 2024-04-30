from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:comoestan@localhost/hackathon'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secretkey = '07492149d856d457df9a8baf19a625f7'

db = SQLAlchemy(app)
ma = Marshmallow(app)