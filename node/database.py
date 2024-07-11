import time

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped

engine = create_engine('sqlite:///blockchain.db', echo=False)
Base = declarative_base()


class Block(Base):
    __tablename__ = 'blocks'

    index: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int] = mapped_column()
    nonce: Mapped[int] = mapped_column()
    previous_hash: Mapped[str] = mapped_column()
    transactions = relationship("Transaction", back_populates="block")

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'previous_hash': self.previous_hash,
            'transactions': [transaction.to_dict() for transaction in self.transactions],
        }

    def __init__(self, block: dict[id:int, timestamp:int, nonce:int, previous_hash:str]):
        self.index = block["index"]
        self.timestamp = block["timestamp"]
        self.nonce = block["nonce"]
        self.previous_hash = block["previous_hash"]


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[float] = mapped_column()
    sender: Mapped[str] = mapped_column()
    recipient: Mapped[str] = mapped_column()
    amount: Mapped[float] = mapped_column()
    fee: Mapped[float] = mapped_column()
    public_key: Mapped[str] = mapped_column()
    sign: Mapped[str] = mapped_column()
    block_id = mapped_column(ForeignKey("blocks.index"))
    block = relationship("Block", back_populates="transactions")

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'fee': self.fee,
            'public_key': self.public_key,
            'sign': self.sign,
        }

    def __init__(self, transaction: dict[timestamp:int, sender:str, recipient:str, amount:float, fee:float]):
        self.timestamp = transaction["timestamp"]
        self.sender = transaction["sender"]
        self.recipient = transaction["recipient"]
        self.amount = transaction["amount"]
        self.fee = transaction["fee"]
        self.public_key = transaction["public_key"]
        self.sign = transaction["sign"]
        self.block_id = transaction["block_id"]


#
# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
# generic_block = {
#     "index": 0,
#     "timestamp": time.time(),
#     "nonce": 100,
#     "previous_hash": "",
# }
# block = Block(generic_block)
# session.add(block)
# session.commit()
# session.close()
