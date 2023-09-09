from strenum import StrEnum


class StrLowerEnum(StrEnum):
    @classmethod
    def _missing_(cls: "StrLowerEnum", value: str) -> "StrLowerEnum":
        for member in cls:
            if member.value == value.lower():
                return member
        raise ValueError(f"'{value}' is not a valid {type(cls).__name__}")


class Axis(StrLowerEnum):
    X = "x"
    Y = "y"
    Z = "z"


class Bool(StrLowerEnum):
    TRUE = "true"
    FALSE = "false"


class Direction(StrLowerEnum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    UP = "up"
    DOWN = "down"


class Face(StrLowerEnum):
    WALL = "wall"
    FLOOR = "floor"
    CEILING = "ceiling"


class PropNames(StrLowerEnum):
    ATTACHMENT = "attachment"
    FACE = "face"
    FACING = "facing"
    HALF = "half"
    HINGE = "hinge"
    SHAPE = "shape"
    TYPE = "type"
    VERTICAL_DIRECTION = "vertical_direction"
