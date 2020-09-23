import hashlib
import json
from time import time
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, request

class Blockchain:
    def __init__(self):
        self.receiving_votes = []
        self.chain = []
        self.nodes = set()

        # Create the header
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def uniq_in_chain(self,token_id):
        chain = self.chain
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            for each_vote in block['votes']:
                if token_id == each_vote['token_id']:
                    return False
            current_index += 1
        return True

    def stored_votes(self):
        chain = self.chain
        current_index = 1
        results = {}
        while current_index < len(chain):
            block = chain[current_index]
            for each_vote in block['votes']:
                if not each_vote['selection'] in results:
                    results[each_vote['selection']] = 0
                results[each_vote['selection']] += 1
            current_index += 1
        return results

    def uniq_in_buf(self,token_id):
        if token_id in self.get_token_id():
            return False
        return True

    def uniq_in_neighbor(self,token_id):
        for node in self.nodes:
            response = requests.get(f'http://{node}/token_id')
            if "%d" % token_id in response.json().keys():
                return False
        return True

    def get_token_id(self):
        return set(map(lambda x: x['token_id'],self.receiving_votes))

    def propagate(self):

        new_chain = None
        max_length = len(self.chain)

        # verify chained stores from all the registered nodes and pick the longest chain
        for node in self.nodes:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'votes': self.receiving_votes,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of votes
        self.receiving_votes = []
        self.chain.append(block)
        return block

    def new_vote(self, token_id, selection):
        self.receiving_votes.append({
            'token_id': token_id,
            'selection': selection 
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        
        # Proof of Work Algorithm:
        # Find a number p' such that hash(pp') contains leading 4 zeroes
        # Where p is the previous proof, and p' is the new proof
         
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Instantiate the Node
app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/vote', methods=['POST'])
def vote():
    values = request.get_json()
    required = ['token_id', 'selection']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Check unique of token_id
    token_id = values['token_id']
    if blockchain.uniq_in_chain(token_id) and blockchain.uniq_in_buf(token_id) and blockchain.uniq_in_neighbor(token_id):
        # Create a new vote
        index = blockchain.new_vote(values['token_id'], values['selection'])
        response = {'message': f'the token_id {token_id} vote will be added to Block {index}'}
        return jsonify(response),201
    else:
        response = {'error':f'the token_id {token_id} already voted'}
        return jsonify(response),503

@app.route('/store', methods=['GET'])
def store():
    # copy the longest chain among the registered nodes
    replaced = blockchain.propagate()

    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # Forge the new block with a new vote by adding it to the chain

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'votes': block['votes'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/view_vote', methods=['GET'])
def view_vote():
    return jsonify(blockchain.stored_votes()), 200

@app.route('/token_id', methods=['GET'])
def pull_token_id():
    response= {}
    for each_token_id in  blockchain.get_token_id():
        response[each_token_id] = 1
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    replaced = blockchain.propagate()
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/sync', methods=['GET'])
def sync():
    replaced = blockchain.propagate()

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
