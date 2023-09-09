import os.path

import pytest

from minecraft_object_utils import Axis, BlockFactory, ModInfo

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__), "data")
TEST_NAMESPACE = "test"
VANILLA_JAVA = ModInfo(TEST_NAMESPACE, "1.0", TEST_DIRECTORY)

BLOCK_FACTORY = BlockFactory([VANILLA_JAVA])


def test_invalid_axis() -> None:
    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_east")
    with pytest.raises(ValueError):
        rail.reflect("a")


def test_reflect_block_x() -> None:
    axis = Axis.X

    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_east")
    rail.reflect(axis)
    assert rail.get_state("shape") == "ascending_west"
    rail.reflect(axis)
    assert rail.get_state("shape") == "ascending_east"

    glow_lichen = BLOCK_FACTORY.create(
        "glow_lichen", north="true", east="true", up="true"
    )
    for _ in range(2):
        prev_block = glow_lichen.copy()
        glow_lichen.reflect(axis)
        assert glow_lichen.get_state("east") == prev_block.get_state("west")
        assert glow_lichen.get_state("west") == prev_block.get_state("east")
        assert glow_lichen.get_state("up") == prev_block.get_state("up")
        assert glow_lichen.get_state("down") == prev_block.get_state("down")
        assert glow_lichen.get_state("south") == prev_block.get_state("south")
        assert glow_lichen.get_state("north") == prev_block.get_state("north")

    oak_button = BLOCK_FACTORY.create("oak_button", face="wall", facing="east")
    oak_button.reflect(axis)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "west"
    )
    oak_button.reflect(axis)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "east"
    )

    skull = BLOCK_FACTORY.create("skeleton_skull", rotation=1)
    skull.reflect(axis)
    assert skull.get_state("rotation") == "15"


def test_reflect_block_y() -> None:
    axis = Axis.Y

    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_east")
    rail.reflect(axis)
    assert rail.get_state("shape") == "ascending_west"
    rail.reflect(axis)
    assert rail.get_state("shape") == "ascending_east"

    glow_lichen = BLOCK_FACTORY.create(
        "glow_lichen", north="true", east="true", up="true"
    )
    for _ in range(2):
        prev_block = glow_lichen.copy()
        glow_lichen.reflect(axis)
        assert glow_lichen.get_state("east") == prev_block.get_state("east")
        assert glow_lichen.get_state("west") == prev_block.get_state("west")
        assert glow_lichen.get_state("up") == prev_block.get_state("down")
        assert glow_lichen.get_state("down") == prev_block.get_state("up")
        assert glow_lichen.get_state("south") == prev_block.get_state("south")
        assert glow_lichen.get_state("north") == prev_block.get_state("north")

    oak_button = BLOCK_FACTORY.create("oak_button", face="ceiling", facing="north")
    oak_button.reflect(axis)
    assert (
        oak_button.get_state("face") == "floor"
        and oak_button.get_state("facing") == "north"
    )
    oak_button.reflect(axis)
    assert (
        oak_button.get_state("face") == "ceiling"
        and oak_button.get_state("facing") == "north"
    )

    skull = BLOCK_FACTORY.create("skeleton_skull", rotation=1)
    skull.reflect(axis)
    assert skull.get_state("rotation") == "1"


def test_reflect_block_z() -> None:
    axis = Axis.Z

    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_south")
    rail.reflect(axis)
    assert rail.get_state("shape") == "ascending_north"
    rail.reflect(axis)
    assert rail.get_state("shape") == "ascending_south"

    glow_lichen = BLOCK_FACTORY.create(
        "glow_lichen", north="true", east="true", up="true"
    )
    for _ in range(2):
        prev_block = glow_lichen.copy()
        glow_lichen.reflect(axis)
        assert glow_lichen.get_state("east") == prev_block.get_state("east")
        assert glow_lichen.get_state("west") == prev_block.get_state("west")
        assert glow_lichen.get_state("up") == prev_block.get_state("up")
        assert glow_lichen.get_state("down") == prev_block.get_state("down")
        assert glow_lichen.get_state("south") == prev_block.get_state("north")
        assert glow_lichen.get_state("north") == prev_block.get_state("south")

    oak_button = BLOCK_FACTORY.create("oak_button", face="wall", facing="north")
    oak_button.reflect(axis)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "south"
    )
    oak_button.reflect(axis)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "north"
    )

    skull = BLOCK_FACTORY.create("skeleton_skull", rotation=1)
    skull.reflect(axis)
    assert skull.get_state("rotation") == "7"
