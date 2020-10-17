from sqlalchemy import create_engine, Column, Integer, String, DateTime


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

###
engine = create_engine('sqlite:///BlocksDB.db') # add , echo = True for the logging

###
Base = declarative_base()
###

# Session = sessionmaker(bind=engine)
# session = Session()

class Blocks(Base):

    __tablename__ = 'blocks'

    id          = Column(Integer, primary_key=True)
    data        = Column(String(250))
    hash        = Column(String(90))
    prevHash    = Column(String(90))
    blockNo      = Column(Integer)
    timestamp   = Column(DateTime)

    def __init__(self, blockNo, data, hash, prevHash,timestamp):

        self.data = data
        self.blockNo = blockNo
        self.hash = hash
        self.prevHash = prevHash
        self.timestamp = timestamp


    def __repr__(self):
        return "<Blocks('%s', '%s','%s','%s',','%s')>" % (self.blockNo,
                                                          self.data,
                                                          str(self.hash),
                                                          self.prevHash,
                                                          self.timestamp)

