import os.path

import pytest

from minecraft_object_utils import ItemFactory, ItemStack, ModInfo

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__), "data")
TEST_NAMESPACE = "test"
VANILLA_JAVA = ModInfo(TEST_NAMESPACE, "1.0", TEST_DIRECTORY)

ITEM_FACTORY = ItemFactory([VANILLA_JAVA])


@pytest.fixture
def test_item() -> ItemStack:
    return ITEM_FACTORY.create("wooden_shovel")


def test_set_valid_count(test_item: ItemStack) -> None:
    test_item.count = 1
    assert test_item.count == 1
    assert test_item.count <= test_item.traits.max_stack_size


def test_set_invalid_count(test_item: ItemStack) -> None:
    with pytest.raises(ValueError):
        test_item.count = 100


def test_set_valid_damage(test_item: ItemStack) -> None:
    test_item.damage = 10
    assert test_item.damage == 10
    assert test_item.damage <= test_item.traits.max_damage


def test_set_invalid_damage(test_item: ItemStack) -> None:
    with pytest.raises(ValueError):
        test_item.damage = 1000
