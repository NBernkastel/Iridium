import hashlib
import json
import time

from Utils.keygen import sign_ecdsa_msg, validate_address_signature
from node.database import session, Block, Transaction


class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.difficult = 5
        self.address = "ir1q256k4qv6taavm9wf3pgwx33esleq8re8z3g87e"
        self.public_key = "TrJzTKoeKSpNoUah3xs3+bSid7xWDppaJu57kWGtuKtcb6XJg8hcSG/kMm691XZ3SUzOtto+1Dp4nVXGYfxHPw=="
        self.private_key = "i35F38GaMFv+ZSjUlYxXAtPcr8jsn5I0jSy5/osHBb4="
        # self.nodes = set()

    def valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficult] == "00000"

    def get_last_block(self):
        block = session.query(Block).order_by(Block.index.desc()).first()
        print(block.to_dict())
        return block

    def elem_hash(self, elem: dict) -> str:
        elem_string = json.dumps(elem, sort_keys=True).encode()
        return hashlib.sha256(elem_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    def create_block(self):
        last_block = self.get_last_block()
        block = {
            'index': last_block.index + 1,
            'timestamp': time.time(),
            'nonce': self.proof_of_work(last_block.nonce),
            'previous_hash': self.elem_hash(last_block.to_dict()),
        }
        coinbase = self.create_transaction("0", self.address, 1, 0, self.public_key)
        coinbase["block_id"] = last_block.index + 1
        session.add(Block(block))
        session.add(Transaction(coinbase))
        session.commit()

    def create_transaction(self, sender: str, recipient: str, amount: float, fee: float, public_key: str):
        transaction = {
            'timestamp': time.time(),
            'sender': sender,
            'recipient': recipient,
            'amount': float(amount),
            'fee': float(fee),
            'public_key': public_key
        }
        transaction_hash = self.elem_hash(transaction)
        transaction['sign'] = sign_ecdsa_msg(self.private_key, transaction_hash)
        return transaction

    def validate_transaction(self, transaction):
        sign = transaction['sign']
        del transaction['sign']
        if transaction['sender'] == '0':
            if transaction['amount'] == 1 and transaction['fee'] == 0:
                if validate_address_signature(
                        transaction['recipient'], transaction['public_key'], sign, self.elem_hash(transaction)):
                    return True
                else:
                    return False
            else:
                return False


if __name__ == "__main__":
    blockchain = Blockchain()
    trx = session.query(Transaction).first()
    print(blockchain.create_block())
    # print(blockchain.validate_transaction(trx.to_dict()))
