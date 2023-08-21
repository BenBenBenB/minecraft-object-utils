import pytest

from minecraft_object_utils import Block, BlockFactory

BLOCK_FACTORY = BlockFactory()


@pytest.fixture
def test_block() -> Block:
    return BLOCK_FACTORY.create("note_block")


def test_set_valid_property(test_block: Block) -> None:
    test_block.set_state("note", 10)
    assert test_block.get_state("note") == "10"


def test_set_invalid_property(test_block: Block) -> None:
    with pytest.raises(ValueError):
        test_block.set_state("bad", 10)


def test_set_invalid_state(test_block: Block) -> None:
    with pytest.raises(ValueError):
        test_block.set_state("note", 25)
