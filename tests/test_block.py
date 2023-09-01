import os.path

import pytest

from minecraft_object_utils import Block, BlockFactory, Inventory, ModInfo

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__), "data")
TEST_NAMESPACE = "test"
VANILLA_JAVA = ModInfo(TEST_NAMESPACE, "1.0", TEST_DIRECTORY)

BLOCK_FACTORY = BlockFactory([VANILLA_JAVA])


@pytest.fixture
def test_block() -> Block:
    return BLOCK_FACTORY.create("powered_rail")


@pytest.fixture
def test_block_inventory() -> Block:
    return BLOCK_FACTORY.create("chest")


def test_set_valid_property(test_block: Block) -> None:
    test_block.set_state("powered", True)
    assert test_block.get_state("powered") == "true"


def test_set_invalid_property(test_block: Block) -> None:
    with pytest.raises(ValueError):
        test_block.set_state("bad", 10)


def test_set_invalid_state(test_block: Block) -> None:
    with pytest.raises(ValueError):
        test_block.set_state("powered", 25)


def test_new_block_inventory(test_block_inventory: Block) -> None:
    assert type(test_block_inventory.inventory) is Inventory
    assert len(test_block_inventory.inventory) == 27
    assert not any(test_block_inventory.inventory)
