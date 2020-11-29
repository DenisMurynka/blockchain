from main import app
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blockchain.db'
db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Transaction(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    #__tablename__ = 'blocks'

    data = db.Column(db.String(250))
    hash = db.Column(db.String(90))
    prevHash = db.Column(db.String(90))
    blockNo = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)