#from main import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import sessionmaker

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blockchain.db'
# db = SQLAlchemy(app)
#
# #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Base = declarative_base()
class Transaction(Base):
    id = Column(Integer,primary_key = True,autoincrement=True)
    __tablename__ = 'transaction'

    data = Column(String(250))
    hash = Column(String(90))
    prevHash = Column(String(90))
    transactionNo = Column(Integer)
    timestamp = Column(DateTime)
    #proof = Column(Integer)
    nID_block = Column(Integer,ForeignKey('block.id'))



class Block(Base):
    __tablename__ = 'block'

    id = Column(Integer, primary_key=True,autoincrement=True)
    prevBlockHash = Column(String)
    currBlockHash = Column(String)
    timestamp = Column(DateTime)
