from uuid import uuid4
import random               #including this for testing data
from database import Transaction, sessionmaker, Block
import datetime
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from blockchain_class import Blockchain
engine = create_engine('sqlite:///blockchain.db') # add , echo = True for the logging
Session = sessionmaker(bind=engine)
session = Session()

Session1 = sessionmaker(bind=engine)
session1 = Session()
# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

currentTime = datetime.datetime.now()
@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=random.randint(1, 1000000),
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    current_block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        #'index': current_block['index'],
        'index': (session.query(Block.id).order_by(Block.id.desc()).first())[0]+1,
        'transactions': current_block['transactions'],
        'proof': current_block['proof'],
        'previous_hash': current_block['previous_hash'],
    }
    session1.add(
        Block(
            id=(session.query(Block.id).order_by(Block.id.desc()).first())[0]+1,
            currBlockHash=blockchain.hash(current_block),
            prevBlockHash=blockchain.hash(last_block),
            timestamp=currentTime
        )
    )
    # session.add(
    #     Transaction(
    #         id=(session.query(Transaction.id).order_by(Transaction.id.desc()).first())[0]+1,
    #         data="New Block Forged",
    #         transactionNo= current_block['index'],
    #         hash=blockchain.hash(current_block),
    #         prevHash=current_block['previous_hash'],
    #         timestamp=currentTime,
    #         proof=current_block['proof'],
    #         nID_block=3
    #     )
    # )

    session1.commit()    # id does not increase because of there is no id increasing via insert aka commit
    #session.commit()
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    #index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}

    session.add(
        Transaction(
            id=(session.query(Transaction.id).order_by(Transaction.id.desc()).first())[0]+1,
            data=values['amount'],
            transactionNo= (session.query(Transaction.id).order_by(Transaction.id.desc()).first())[0]+1,
            hash=blockchain.hash(str(values['sender'])+str(values['recipient'])+ str(values['amount'])),
            prevHash='#####',#how to get prev hash?
            timestamp=currentTime,
            #proof=current_block['proof'],
            nID_block=(session.query(Block.id).order_by(Block.id.desc()).first())[0]+1
        )
    )


    session.commit()

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain

    }

    print(blockchain)
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)