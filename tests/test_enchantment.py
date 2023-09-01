import os.path

import pytest

from minecraft_object_utils import Enchantment, EnchantmentFactory, ModInfo

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__), "data")
TEST_NAMESPACE = "test"
VANILLA_JAVA = ModInfo(TEST_NAMESPACE, "1.0", TEST_DIRECTORY)

ENTITY_FACTORY = EnchantmentFactory([VANILLA_JAVA])


@pytest.fixture
def test_enchantment() -> Enchantment:
    return ENTITY_FACTORY.create("protection")


def test_enchantment_loaded(test_enchantment: Enchantment) -> None:
    assert test_enchantment.traits.max_level == 4
    assert test_enchantment.traits.category == "ARMOR"
    assert test_enchantment.traits.rarity == "COMMON"
    assert not test_enchantment.traits.curse


def test_set_level(test_enchantment: Enchantment) -> None:
    assert test_enchantment.level == 1
    for i in range(1, test_enchantment.traits.max_level + 1):
        test_enchantment.level = i
        assert test_enchantment.level == i


def test_set_invalid_level(test_enchantment: Enchantment) -> None:
    with pytest.raises(ValueError):
        test_enchantment.level = 0
    with pytest.raises(ValueError):
        test_enchantment.level = test_enchantment.traits.max_level + 1
