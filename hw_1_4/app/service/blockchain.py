import datetime
import hashlib
import json
import multiprocessing

from functools import partial
from .block import Block, BlockStatus
from .service import BlockchainInterface


def math_func(proof: int, previous_proof: int) -> int:
    return proof ** 2 - previous_proof ** 2


def get_sha256(proof, previous_proof):
    return hashlib.sha256(
        str(math_func(proof, previous_proof)).encode()
    ).hexdigest()


class Blockchain(BlockchainInterface):
    """
    BlockChain
        [data1] -> [data2, hash(data1)] -> [data3, hash(data2)]
        proof-of-work --
        blockchain - nodes(компы)
    """

    def __init__(self, calc_complex="00000"):
        self.chain: [Block] = []
        self._mining_blocks: [int] = []
        self.create_block(1, "0")
        self.complex = calc_complex

    def create_block(self, proof, previous_hash) -> Block:
        block = Block(
            index=len(self.chain) + 1,
            previous_hash=previous_hash,
            timestamp=str(datetime.datetime.now()),
            proof=proof,
        )
        self.chain.append(block)

        return block

    def mine_block(self):
        block_index = self.get_next_block_index()

        if block_index in self._mining_blocks:
            return

        self._mining_blocks.append(block_index)

        previous_block = self.get_previous_block()
        previous_proof = previous_block.proof

        proof = self.proof_of_work(previous_proof)
        previous_hash = self.make_hash(previous_block)

        block = self.create_block(proof, previous_hash)
        self._mining_blocks.remove(block_index)

        return block

    def get_previous_block(self):
        return self.chain[-1]

    def make_hash(self, block):
        encoded_block = json.dumps(block.toDict(), sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def _proof_of_work(self, previous_proof, new_proof=1):
        check_proof = False

        while check_proof is False:
            hash_operation = get_sha256(new_proof, previous_proof)

            if self.is_hash_complex_valid(hash_operation):
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def proof_of_work(self, previous_proof):
        step = 5 * 10**len(self.complex)
        workers = multiprocessing.cpu_count()
        with multiprocessing.Pool(processes=workers) as pool:
            result = pool.imap_unordered(partial(
                self._proof_of_work, previous_proof
            ), list(range(1, 10 * step, step)))

            return next(result)

    def is_hash_complex_valid(self, hash_operation):
        return hash_operation[:len(self.complex)] == self.complex

    def is_chain_valid(self):
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block.previous_hash != self.make_hash(previous_block):
                return False

            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = get_sha256(proof, previous_proof)

            if not self.is_hash_complex_valid(hash_operation):
                return False

            previous_block = block
            block_index += 1

        return True

    def get_chain(self):
        return self.chain

    def get_block_status(self, block_id):
        if block_id in [block.index for block in self.chain]:
            return BlockStatus.COMPLETED
        elif block_id in self._mining_blocks:
            return BlockStatus.IN_PROGRESS
        else:
            return BlockStatus.NOT_FOUND

    def get_next_block_index(self):
        return len(self.chain) + 1
