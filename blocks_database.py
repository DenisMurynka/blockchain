from sqlalchemy import create_engine, Column, Integer, String, DateTime


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

###
engine = create_engine('sqlite:///telegrambotDB.db', echo = True)

###
Base = declarative_base()
###

# Session = sessionmaker(bind=engine)
# session = Session()

class Blocks(Base):

    __tablename__ = 'users'

    id          = Column(Integer, primary_key=True)
    data        = Column(String(250))
    hash        = Column(String(90))
    prevHash    = Column(String(90))
    blockNo = Column(Integer)
    timestamp   = Column(DateTime)

    def __init__(self, blockNo, data, hash, prevHash,timestamp):
        self.blockNo =blockNo
        self.data = data

        self.hash = hash
        self.prevHash = prevHash
        self.timestamp = timestamp


    def __repr__(self):
        return "<Users('%s', '%s','%s')>" % (self.name, self.lastname, self.username)


class Using(Base):
    __tablename__ = 'using'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(50))
    lastname    = Column(String(50))
    username    = Column(String(50))
    songname = Column(String(50))
    date     = Column(DateTime)

    def __init__(self, name, lastname, username,songname, date):
        self.name = name
        self.lastname = lastname
        self.username = username
        self.songname = songname
        self.date = date

    def __repr__(self):
        return "<Users('%s', '%s','%s','%s')>" % (self.name, self.lastname, self.username,self.date)



#meta.create_all(engine) #run once time