import datetime
import hashlib
from blocks_database import Blocks, engine, sessionmaker
import logging

from sqlalchemy.exc import OperationalError, ProgrammingError

from flask import Flask, jsonify, request
from uuid import uuid4

from sqlalchemy import column

Session = sessionmaker(bind=engine)
session = Session()

logging.basicConfig(filename='sqlalchemyLogging.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

log = logging.getLogger("ERROR --------> ")

app = Flask(__name__)


# Генерируем уникальный на глобальном уровне адрес для этого узла
node_identifier = str(uuid4()).replace('-', '')

class Block:
    # c = session.query(Blocks).order_by(Blocks.id.desc()).limit(2)     #hot ot get last one row in db
    # c = c[::-1]
    #dbObj = Blocks


    blockNo = (session.query(Blocks.blockNo).order_by(Blocks.id.desc()).first())[0]
    data = None
    next = None
    hash = None


    nonce = 0
    #previous_hash = 0x0
    previous_hash = (session.query(Blocks.prevHash).order_by(Blocks.id.desc()).first())[0]
    timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data



    def hash(self):

        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8')
        )

        return h.hexdigest()



    def __str__(self):
        block = {
            'index': str(self.blockNo),
            'timestamp': str(self.timestamp),
            'transactions':  str(self.data).encode('utf-8'),
            'previous_hash': str(self.previous_hash).encode('utf-8'),
        }
        return "Block Hash: " + str(self.hash()) + \
               "\nBlockNo: " + str(self.blockNo) + \
               "\nBlock Data: " + str(self.data) + \
               "\nHashes: " + str(self.nonce) + \
               "\n--------------"
       # return jsonify(block), 200


class Blockchain:


    diff = 10
    maxNonce = 2 ** 32
    target = 2 ** (256 - diff)

    block = Block("Genesis")
   # dummy = head = block

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next

    # def __str__(self):
    #     return self
    # def valid_check(self):



    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)

                print(block)
                #print(str(column('id') == 967 ))

                session.add(
                    Blocks(

                        data=str(block.data),
                        blockNo=str(block.blockNo),
                        hash=str(block.hash()),
                        prevHash=str(block.previous_hash).encode('utf-8'),
                        timestamp=block.timestamp
                    )
                )
                session.commit()



                logging.exception("Exception occurred")
                log.exception(block)
                break
            else:
                block.nonce += 1

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():#http://127.0.0.0/mine


    return "We'll mine a new Block"



if __name__ == '__main__':

    try :
        #app.run()

        for n in range(10):
        #     # blockchain.mine(Block(Block("Block " + str((session.query(Blocks.blockNo).order_by(Blocks.id.desc()).first())[0]))))
        #     # blockchain.mine(Block(Block("some data")))
            blockchain.mine(Block("some data"))

        # while blockchain.head != None:
        #     blockchain.head = blockchain.head.next



    except (ProgrammingError, OperationalError) as e:
        logging.exception("Exception occurred")
        log.exception(e)

    except Exception as e:
        logging.exception("Exception occurred")
        #log.exception(e)




#obj = session.query(Blocks.blockNo).order_by(Blocks.id.desc()).first()

#print((session.query(Blocks.blockNo).order_by(Blocks.id.desc()).first())[0])