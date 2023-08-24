import os.path

import pytest

from minecraft_object_utils import Entity, EntityFactory, ModInfo

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__), "data")
TEST_NAMESPACE = "test"
VANILLA_JAVA = ModInfo(TEST_NAMESPACE, "1.0", TEST_DIRECTORY)

ENTITY_FACTORY = EntityFactory([VANILLA_JAVA])


@pytest.fixture
def test_entity() -> Entity:
    return ENTITY_FACTORY.create("blaze")


def test_entity_loaded(test_entity: Entity) -> None:
    assert test_entity.traits.category == "MONSTER"
    assert test_entity.traits.width == 0.6
    assert test_entity.traits.height == 1.8
    assert test_entity.traits.fire_immune is True
