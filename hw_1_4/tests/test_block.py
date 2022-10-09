import pytest

from hw_1_4.app.service.block import Block


@pytest.mark.parametrize("index", [1])
@pytest.mark.parametrize("previous_hash", ["0"])
@pytest.mark.parametrize("timestamp", ["2020-01-01 00:00:00"])
@pytest.mark.parametrize("proof", [1])
def test_block_init(index, previous_hash, timestamp, proof):
    block = Block(index, previous_hash, timestamp, proof)
    assert block.index == index
    assert block.previous_hash == previous_hash
    assert block.timestamp == timestamp
    assert block.proof == proof


@pytest.mark.parametrize("index", [1])
@pytest.mark.parametrize("previous_hash", ["0"])
@pytest.mark.parametrize("timestamp", ["2020-01-01 00:00:00"])
@pytest.mark.parametrize("proof", [1])
def test_block_to_dict(index, previous_hash, timestamp, proof):
    block = Block(index, previous_hash, timestamp, proof)
    assert block.toDict() == {
        "index": index,
        "previous_hash": previous_hash,
        "timestamp": timestamp,
        "proof": proof,
    }
