import os.path

import pytest

from minecraft_object_utils import Axis, Block, BlockFactory, ModInfo

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__), "data")
TEST_NAMESPACE = "test"
VANILLA_JAVA = ModInfo(TEST_NAMESPACE, "1.0", TEST_DIRECTORY)

BLOCK_FACTORY = BlockFactory([VANILLA_JAVA])


@pytest.fixture
def test_block_rail() -> Block:
    return BLOCK_FACTORY.create("powered_rail")


@pytest.fixture
def test_block_direction_props() -> Block:
    return BLOCK_FACTORY.create("vine")


@pytest.fixture
def test_block_face_facing() -> Block:
    return BLOCK_FACTORY.create("oak_button")


@pytest.fixture
def test_block_rotation_prop() -> Block:
    return BLOCK_FACTORY.create("skeleton_skull")


def test_invalid_axis(test_block_rail: Block) -> None:
    with pytest.raises(ValueError):
        test_block_rail.rotate("a", 90)


def test_invalid_angle(test_block_rail: Block) -> None:
    for angle in [0, 45, 360]:
        with pytest.raises(ValueError):
            test_block_rail.rotate(Axis.X, angle)


def test_rotate_block_x_90() -> None:
    axis = Axis.X
    angle = 90

    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_north")
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_south"

    glow_lichen = BLOCK_FACTORY.create(
        "glow_lichen", north="true", east="true", up="true"
    )
    for _ in range(4):
        prev_block = glow_lichen.copy()
        glow_lichen.rotate(axis, angle)
        assert glow_lichen.get_state("up") == prev_block.get_state("north")
        assert glow_lichen.get_state("south") == prev_block.get_state("up")
        assert glow_lichen.get_state("down") == prev_block.get_state("south")
        assert glow_lichen.get_state("north") == prev_block.get_state("down")
        assert glow_lichen.get_state("east") == prev_block.get_state("east")
        assert glow_lichen.get_state("west") == prev_block.get_state("west")

    oak_button = BLOCK_FACTORY.create("oak_button", face="wall", facing="south")
    oak_button.rotate(axis, angle)
    assert oak_button.get_state("face") == "ceiling"
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "north"
    )
    oak_button.rotate(axis, angle)
    assert oak_button.get_state("face") == "floor"
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "south"
    )

    skull = BLOCK_FACTORY.create("skeleton_skull", rotation=1)
    skull.rotate(axis, angle)
    assert skull.get_state("rotation") == "1"


def test_rotate_block_x_180() -> None:
    axis = Axis.X
    angle = 180

    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_north")
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_north"

    glow_lichen = BLOCK_FACTORY.create(
        "glow_lichen", north="true", east="true", up="true"
    )
    for _ in range(2):
        prev_block = glow_lichen.copy()
        glow_lichen.rotate(axis, angle)
        assert glow_lichen.get_state("up") == prev_block.get_state("down")
        assert glow_lichen.get_state("south") == prev_block.get_state("north")
        assert glow_lichen.get_state("down") == prev_block.get_state("up")
        assert glow_lichen.get_state("north") == prev_block.get_state("south")
        assert glow_lichen.get_state("east") == prev_block.get_state("east")
        assert glow_lichen.get_state("west") == prev_block.get_state("west")

    oak_button = BLOCK_FACTORY.create("oak_button", face="wall", facing="north")
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "south"
    )
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "north"
    )

    skull = BLOCK_FACTORY.create("skeleton_skull", rotation=1)
    skull.rotate(axis, angle)
    assert skull.get_state("rotation") == "7"


def test_rotate_block_x_270() -> None:
    axis = Axis.X
    angle = 270

    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_north")
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_south"

    glow_lichen = BLOCK_FACTORY.create(
        "glow_lichen", north="true", east="true", up="true"
    )
    for _ in range(4):
        prev_block = glow_lichen.copy()
        glow_lichen.rotate(axis, angle)

        assert glow_lichen.get_state("up") == prev_block.get_state("south")
        assert glow_lichen.get_state("south") == prev_block.get_state("down")
        assert glow_lichen.get_state("down") == prev_block.get_state("north")
        assert glow_lichen.get_state("north") == prev_block.get_state("up")
        assert glow_lichen.get_state("east") == prev_block.get_state("east")
        assert glow_lichen.get_state("west") == prev_block.get_state("west")

    oak_button = BLOCK_FACTORY.create("oak_button", face="wall", facing="south")
    oak_button.rotate(axis, angle)
    assert oak_button.get_state("face") == "floor"
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "north"
    )
    oak_button.rotate(axis, angle)
    assert oak_button.get_state("face") == "ceiling"
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "south"
    )

    skull = BLOCK_FACTORY.create("skeleton_skull", rotation=1)
    skull.rotate(axis, angle)
    assert skull.get_state("rotation") == "1"


def test_rotate_block_y_90() -> None:
    axis = Axis.Y
    angle = 90

    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_east")
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_north"
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_west"
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_south"
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_east"

    glow_lichen = BLOCK_FACTORY.create(
        "glow_lichen", north="true", east="true", up="true"
    )
    for _ in range(4):
        prev_block = glow_lichen.copy()
        glow_lichen.rotate(axis, angle)
        assert glow_lichen.get_state("north") == prev_block.get_state("east")
        assert glow_lichen.get_state("east") == prev_block.get_state("south")
        assert glow_lichen.get_state("south") == prev_block.get_state("west")
        assert glow_lichen.get_state("west") == prev_block.get_state("north")
        assert glow_lichen.get_state("up") == prev_block.get_state("up")
        assert glow_lichen.get_state("down") == prev_block.get_state("down")

    oak_button = BLOCK_FACTORY.create("oak_button", face="wall", facing="north")
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "west"
    )
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "south"
    )
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "east"
    )
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "north"
    )

    skull = BLOCK_FACTORY.create("skeleton_skull", rotation=1)
    skull.rotate(axis, angle)
    assert skull.get_state("rotation") == "13"


def test_rotate_block_y_180() -> None:
    axis = Axis.Y
    angle = 180

    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_east")
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_west"
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_east"

    glow_lichen = BLOCK_FACTORY.create(
        "glow_lichen", north="true", east="true", up="true"
    )
    for _ in range(2):
        prev_block = glow_lichen.copy()
        glow_lichen.rotate(axis, angle)
        assert glow_lichen.get_state("north") == prev_block.get_state("south")
        assert glow_lichen.get_state("east") == prev_block.get_state("west")
        assert glow_lichen.get_state("south") == prev_block.get_state("north")
        assert glow_lichen.get_state("west") == prev_block.get_state("east")
        assert glow_lichen.get_state("up") == prev_block.get_state("up")
        assert glow_lichen.get_state("down") == prev_block.get_state("down")

    oak_button = BLOCK_FACTORY.create("oak_button", face="wall", facing="north")
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "south"
    )
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "north"
    )

    skull = BLOCK_FACTORY.create("skeleton_skull", rotation=1)
    skull.rotate(axis, angle)
    assert skull.get_state("rotation") == "9"


def test_rotate_block_y_270() -> None:
    axis = Axis.Y
    angle = 270

    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_east")
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_south"
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_west"
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_north"
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_east"

    glow_lichen = BLOCK_FACTORY.create(
        "glow_lichen", north="true", east="true", up="true"
    )
    for _ in range(4):
        prev_block = glow_lichen.copy()
        glow_lichen.rotate(axis, angle)
        assert glow_lichen.get_state("north") == prev_block.get_state("west")
        assert glow_lichen.get_state("east") == prev_block.get_state("north")
        assert glow_lichen.get_state("south") == prev_block.get_state("east")
        assert glow_lichen.get_state("west") == prev_block.get_state("south")
        assert glow_lichen.get_state("up") == prev_block.get_state("up")
        assert glow_lichen.get_state("down") == prev_block.get_state("down")

    oak_button = BLOCK_FACTORY.create("oak_button", face="wall", facing="north")
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "east"
    )
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "south"
    )
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "west"
    )
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "north"
    )

    skull = BLOCK_FACTORY.create("skeleton_skull", rotation=1)
    skull.rotate(axis, angle)
    assert skull.get_state("rotation") == "5"


def test_rotate_block_z_90() -> None:
    axis = Axis.Z
    angle = 90

    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_east")
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_west"

    glow_lichen = BLOCK_FACTORY.create(
        "glow_lichen", north="true", east="true", up="true"
    )
    for _ in range(4):
        prev_block = glow_lichen.copy()
        glow_lichen.rotate(axis, angle)
        assert glow_lichen.get_state("up") == prev_block.get_state("east")
        assert glow_lichen.get_state("west") == prev_block.get_state("up")
        assert glow_lichen.get_state("down") == prev_block.get_state("west")
        assert glow_lichen.get_state("east") == prev_block.get_state("down")
        assert glow_lichen.get_state("north") == prev_block.get_state("north")
        assert glow_lichen.get_state("south") == prev_block.get_state("south")

    oak_button = BLOCK_FACTORY.create("oak_button", face="wall", facing="west")
    oak_button.rotate(axis, angle)
    assert oak_button.get_state("face") == "ceiling"
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "east"
    )
    oak_button.rotate(axis, angle)
    assert oak_button.get_state("face") == "floor"
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "west"
    )

    skull = BLOCK_FACTORY.create("skeleton_skull", rotation=1)
    skull.rotate(axis, angle)
    assert skull.get_state("rotation") == "1"


def test_rotate_block_z_180() -> None:
    axis = Axis.Z
    angle = 180

    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_west")
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_west"

    glow_lichen = BLOCK_FACTORY.create(
        "glow_lichen", north="true", east="true", up="true"
    )
    for _ in range(2):
        prev_block = glow_lichen.copy()
        glow_lichen.rotate(axis, angle)
        assert glow_lichen.get_state("up") == prev_block.get_state("down")
        assert glow_lichen.get_state("west") == prev_block.get_state("east")
        assert glow_lichen.get_state("down") == prev_block.get_state("up")
        assert glow_lichen.get_state("east") == prev_block.get_state("west")
        assert glow_lichen.get_state("north") == prev_block.get_state("north")
        assert glow_lichen.get_state("south") == prev_block.get_state("south")

    oak_button = BLOCK_FACTORY.create("oak_button", face="wall", facing="west")
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "east"
    )
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "west"
    )

    skull = BLOCK_FACTORY.create("skeleton_skull", rotation=1)
    skull.rotate(axis, angle)
    assert skull.get_state("rotation") == "15"


def test_rotate_block_z_270() -> None:
    axis = Axis.Z
    angle = 270

    rail = BLOCK_FACTORY.create("powered_rail", shape="ascending_east")
    rail.rotate(axis, angle)
    assert rail.get_state("shape") == "ascending_west"

    glow_lichen = BLOCK_FACTORY.create(
        "glow_lichen", north="true", east="true", up="true"
    )
    for _ in range(4):
        prev_block = glow_lichen.copy()
        glow_lichen.rotate(axis, angle)
        assert glow_lichen.get_state("up") == prev_block.get_state("west")
        assert glow_lichen.get_state("west") == prev_block.get_state("down")
        assert glow_lichen.get_state("down") == prev_block.get_state("east")
        assert glow_lichen.get_state("east") == prev_block.get_state("up")
        assert glow_lichen.get_state("north") == prev_block.get_state("north")
        assert glow_lichen.get_state("south") == prev_block.get_state("south")

    oak_button = BLOCK_FACTORY.create("oak_button", face="wall", facing="west")
    oak_button.rotate(axis, angle)
    assert oak_button.get_state("face") == "floor"
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "east"
    )
    oak_button.rotate(axis, angle)
    assert oak_button.get_state("face") == "ceiling"
    oak_button.rotate(axis, angle)
    assert (
        oak_button.get_state("face") == "wall"
        and oak_button.get_state("facing") == "west"
    )

    skull = BLOCK_FACTORY.create("skeleton_skull", rotation=1)
    skull.rotate(axis, angle)
    assert skull.get_state("rotation") == "1"
