import datetime
import hashlib
from blocks_database import Blocks, engine, sessionmaker
import logging

Session = sessionmaker(bind=engine)
session = Session()



logging.basicConfig(filename='logging.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
log = logging.getLogger("ex")
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
        # self.hashh = self.hash()
        # print("HASHH  "+str(self.hashh))


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

        return "Block Hash: " + str(self.hash()) + \
               "\nBlockNo: " + str(self.blockNo) + \
               "\nBlock Data: " + str(self.data) + \
               "\nHashes: " + str(self.nonce) + \
               "\n--------------"


class Blockchain:


    diff = 10
    maxNonce = 2 ** 32
    target = 2 ** (256 - diff)

    block = Block("Genesis")
    dummy = head = block

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next



    # def valid_check(self):
    #
    #     #if self.block.previous_hash != self.block.hash:
    #       #  return  False
    #     if self.block.hash == self.block.hash():
    #         print("False")


    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                #print("Prev Hash:" + str(block.previous_hash))
                print(block)


                session.add(
                    Blocks(

                        data=str(block.data),
                        blockNo=str(block.blockNo),
                        hash = str( block.hash()) ,
                        prevHash=str(block.previous_hash).encode('utf-8'),
                        timestamp=block.timestamp
                    )
                )
                session.commit()

                break
            else:
                block.nonce += 1

blockchain = Blockchain()


if __name__ == '__main__':

    try :
        for n in range(10):

            #blockchain.mine(Block(Block("Block " + str((session.query(Blocks.blockNo).order_by(Blocks.id.desc()).first())[0]))))
            #blockchain.mine(Block(Block("some data")))
            blockchain.mine(Block("some data"))

        while blockchain.head != None:
            #print(blockchain.head)
            blockchain.head = blockchain.head.next
    except Exception as e:
        logging.exception("Exception occurred")
        log.exception(e)




#obj = session.query(Blocks.blockNo).order_by(Blocks.id.desc()).first()

#print((session.query(Blocks.blockNo).order_by(Blocks.id.desc()).first())[0])