import datetime
import hashlib
from blocks_database import Blocks, engine, sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

class Block:
    # c = session.query(Blocks).order_by(Blocks.id.desc()).limit(2)     #hot ot get last one row in db
    # c = c[::-1]

    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
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
       # print("NEEDED ro2" + str(self.c)+'\n')
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\n--------------"


class Blockchain:



    #blockDb = Blocks()
    diff = 20
    maxNonce = 2 ** 32
    target = 2 ** (256 - diff)
    block = Block("Genesis")
    dummy = head = block

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print(block)

                session.add(
                    Blocks(
                        blockNo=str(block.blockNo),
                        data=str(block.data),
                        hash = str(block.hash()) ,
                        prevHash=str(block.previous_hash).encode('utf-8'),
                        timestamp=block.timestamp
                    )
                )

                # session.add(
                #    # Blocks(
                #         str(block.blockNo),
                #         str(block.data),
                #         str(block.hash()),
                #         str(block.previous_hash).encode('utf-8'),
                #         block.timestamp
                #    # )
                # )

                break
            else:
                block.nonce += 1

blockchain = Blockchain()

for n in range(10):
    blockchain.mine(Block(Block("Block " + str(n+1))))

while blockchain.head != None:
    print(blockchain.head)
    blockchain.head = blockchain.head.next

    session.commit()
