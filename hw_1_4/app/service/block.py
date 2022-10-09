import json

from enum import Enum


class BlockStatus(Enum):
    """Block status enum"""
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    NOT_FOUND = "NOT_FOUND"


class Block:
    """
    A single block of our blockchain

    Attributes:
        index (int): The index of the block in the blockchain
        previous_hash (str): The hash of the previous block in the blockchain
        timestamp (int): The time the block was created
        proof (int): The proof of work for the block
    """

    def __init__(self, index, previous_hash, timestamp, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.proof = proof

    def toDict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "proof": self.proof,
        }
