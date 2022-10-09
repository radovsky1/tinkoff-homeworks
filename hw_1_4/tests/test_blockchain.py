import pytest
import threading

from hw_1_4.app.service.blockchain import Blockchain, BlockStatus

from hw_1_4.app.service.blockchain import get_sha256


def test_blockchain_init():
    blockchain = Blockchain()
    assert len(blockchain.chain) == 1
    assert blockchain._mining_blocks == []
    assert blockchain.complex == "00000"


def test_blockchain_create_block():
    blockchain = Blockchain()
    block = blockchain.create_block(1, "0")
    assert block.index == 2
    assert block.previous_hash == "0"
    assert block.timestamp
    assert block.proof == 1


@pytest.mark.parametrize("previous_proof", [1])
@pytest.mark.parametrize("complexity", ["00000"])
def test_default_proof_of_work(previous_proof, complexity):
    blockchain = Blockchain(complexity)
    proof = blockchain._proof_of_work(previous_proof)
    assert get_sha256(proof, previous_proof).startswith(blockchain.complex)


@pytest.mark.parametrize("previous_proof", [1])
@pytest.mark.parametrize("complexity", ["00000", "000000"])
def test_proof_of_work(previous_proof, complexity):
    blockchain = Blockchain(complexity)
    proof = blockchain.proof_of_work(previous_proof)
    assert get_sha256(proof, previous_proof).startswith(blockchain.complex)


def test_get_previous_block():
    blockchain = Blockchain()
    block = blockchain.get_previous_block()
    assert block.index == 1
    assert block.previous_hash == "0"
    assert block.timestamp
    assert block.proof == 1


@pytest.mark.parametrize("blocks_to_mine", [2, 3])
def test_is_chain_valid(blocks_to_mine):
    blockchain = Blockchain()
    for _ in range(blocks_to_mine):
        blockchain.mine_block()
    assert blockchain.is_chain_valid() is True


@pytest.mark.parametrize("blocks_to_mine", [3])
def test_is_chain_valid_with_invalid_proof(blocks_to_mine):
    blockchain = Blockchain()
    for _ in range(blocks_to_mine):
        blockchain.mine_block()
    blockchain.chain[-1].proof = 1
    assert blockchain.is_chain_valid() is False


@pytest.mark.parametrize("blocks_to_mine", [3])
def test_is_chain_valid_with_invalid_previous_hash(blocks_to_mine):
    blockchain = Blockchain()
    for _ in range(blocks_to_mine):
        blockchain.mine_block()
    blockchain.chain[-1].previous_hash = "1"
    assert blockchain.is_chain_valid() is False


def test_get_block_status():
    blockchain = Blockchain(calc_complex="000000")
    assert blockchain.get_block_status(2) == BlockStatus.NOT_FOUND
    t = threading.Thread(target=blockchain.mine_block)
    t.start()
    assert blockchain.get_block_status(2) == BlockStatus.IN_PROGRESS
    t.join()
    assert blockchain.get_block_status(2) == BlockStatus.COMPLETED


def test_get_chain():
    blockchain = Blockchain()
    assert len(blockchain.get_chain()) == 1
    blockchain.mine_block()
    assert len(blockchain.get_chain()) == 2
