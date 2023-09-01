import os.path

import pytest

from minecraft_object_utils import Inventory, ItemFactory, ItemStack, ModInfo

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__), "data")
TEST_NAMESPACE = "test"
VANILLA_JAVA = ModInfo(TEST_NAMESPACE, "1.0", TEST_DIRECTORY)

INVENTORY = Inventory(20)
ITEMFACTORY = ItemFactory([VANILLA_JAVA])


@pytest.fixture
def test_items() -> "list[ItemStack]":
    return [
        ITEMFACTORY.create("netherite_block", count=64),
        ITEMFACTORY.create("exposed_copper"),
        ITEMFACTORY.create("wooden_shovel", damage=10),
        None,
        ITEMFACTORY.create("wooden_shovel", damage=10),
    ]


@pytest.fixture
def test_inventory(test_items: "list[ItemStack]") -> Inventory:
    return Inventory.create_from_list(test_items)


def test_de(test_inventory: Inventory) -> None:
    del test_inventory[0]
    assert test_inventory[0] is None
    assert len(test_inventory) == 5


def test_get(test_inventory: Inventory, test_items: ItemStack) -> None:
    assert test_inventory[0] == test_items[0]


def test_get_invalid_slot(test_inventory: Inventory) -> None:
    with pytest.raises(IndexError):
        test_inventory[10]


def test_set(test_inventory: Inventory, test_items: ItemStack) -> None:
    test_inventory[3] = test_items[3]
    assert test_inventory[3] == test_items[3]


def test_set_invalid_slot(test_inventory: Inventory) -> None:
    with pytest.raises(IndexError):
        test_inventory[10] = None


def test_set_invalid_type(test_inventory: Inventory) -> None:
    with pytest.raises(TypeError):
        test_inventory[0] = 7


def test_get_slot(test_inventory: Inventory, test_items: ItemStack) -> None:
    for i in range(-len(test_items), len(test_items)):
        assert test_inventory[i] == test_items[i]


def test_get_slot_invalid_slot(test_inventory: Inventory) -> None:
    with pytest.raises(IndexError):
        test_inventory.get_slot(10)


def test_set_slot(test_inventory: Inventory, test_items: ItemStack) -> None:
    test_inventory.set_slot(1, test_items[4])
    assert test_inventory[1] == test_items[4]


def test_set_slot_invalid_slot(test_inventory: Inventory) -> None:
    with pytest.raises(IndexError):
        test_inventory.set_slot(10, None)


def test_set_slot_invalid_type(test_inventory: Inventory) -> None:
    with pytest.raises(TypeError):
        test_inventory.set_slot(0, "wrong")


def test_contains(test_inventory: Inventory, test_items: ItemStack) -> None:
    for item in test_items:
        assert item in test_inventory
    assert "wrong" not in test_inventory


def test_len(test_inventory: Inventory, test_items: ItemStack) -> None:
    assert len(test_inventory) == len(test_items)


def test_pop(test_inventory: Inventory, test_items: ItemStack) -> None:
    for i in range(len(test_items)):
        assert test_inventory.pop(i) == test_items[i]
        assert test_inventory[i] is None
    assert test_inventory.pop() is None


def test_pop_invalid_slot(test_inventory: Inventory) -> None:
    with pytest.raises(IndexError):
        test_inventory.pop(10)


def test_pop_last(test_inventory: Inventory, test_items: ItemStack) -> None:
    filled_slots = [
        slot for slot in range(len(test_items)) if test_items[slot] is not None
    ]
    filled_slots.reverse()
    for i in filled_slots:
        assert test_inventory.pop() == test_items[i]
        assert test_inventory[i] is None
    assert test_inventory.pop() is None


def test_remove(test_inventory: Inventory, test_items: ItemStack) -> None:
    for i in range(len(test_items)):
        test_inventory.remove(test_items[i])
        assert test_inventory[i] is None
    assert not any(test_inventory)
    assert len(test_inventory) == len(test_items)


def test_clear(test_inventory: Inventory, test_items: ItemStack) -> None:
    test_inventory.clear()
    assert not any(test_inventory)
    assert len(test_inventory) == len(test_items)


def test_count(test_inventory: Inventory, test_items: ItemStack) -> None:
    assert test_inventory.count(test_items[0]) == 1
    assert test_inventory.count(test_items[1]) == 1
    assert test_inventory.count(test_items[2]) == 2
    assert test_inventory.count(test_items[3]) == 1
    assert test_inventory.count(test_items[4]) == 2


def test_index(test_inventory: Inventory, test_items: ItemStack) -> None:
    assert test_inventory.index(test_items[0]) == 0
    assert test_inventory.index(test_items[1]) == 1
    assert test_inventory.index(test_items[2]) == 2
    assert test_inventory.index(test_items[3]) == 3
    assert test_inventory.index(test_items[4]) == 2


def test_reverse(test_inventory: Inventory, test_items: ItemStack) -> None:
    test_inventory.reverse()
    size = len(test_items)
    for i in range(size):
        assert test_inventory[i] == test_items[size - 1 - i]
