from .constants import Axis, Direction, Face


class Reflect:
    X = {
        "facing": [
            ("east", "west"),
            ("west", "east"),
        ],
        "hinge": [
            ("left", "right"),
            ("right", "left"),
        ],
        "rotation": [(str(r), str((16 - r) % 16)) for r in range(16)],
        "shape": [
            ("ascending_east", "ascending_west"),
            ("ascending_west", "ascending_east"),
            ("north_east", "north_west"),
            ("south_east", "south_west"),
            ("north_west", "north_east"),
            ("south_west", "south_east"),
            ("outer_left", "outer_right"),
            ("outer_right", "outer_left"),
            ("inner_left", "inner_right"),
            ("inner_right", "inner_left"),
        ],
    }

    Y = {
        "attachment": [
            ("ceiling", "floor"),
            ("floor", "ceiling"),
        ],
        "face": [
            ("ceiling", "floor"),
            ("floor", "ceiling"),
        ],
        "facing": [
            ("up", "down"),
            ("down", "up"),
        ],
        "half": [
            ("lower", "upper"),
            ("upper", "lower"),
        ],
        "shape": [
            ("ascending_north", "ascending_south"),
            ("ascending_south", "ascending_north"),
            ("ascending_east", "ascending_west"),
            ("ascending_west", "ascending_east"),
        ],
        "type": [
            ("top", "bottom"),
            ("bottom", "top"),
        ],
        "vertical_direction": [
            ("up", "down"),
            ("down", "up"),
        ],
    }

    Z = {
        "facing": [
            ("north", "south"),
            ("south", "north"),
        ],
        "hinge": [
            ("left", "right"),
            ("right", "left"),
        ],
        "rotation": [(str(r), str((24 - r) % 16)) for r in range(16)],
        "shape": [
            ("ascending_north", "ascending_south"),
            ("ascending_south", "ascending_north"),
            ("north_east", "south_east"),
            ("south_east", "north_east"),
            ("north_west", "south_west"),
            ("south_west", "north_west"),
            ("outer_left", "outer_right"),
            ("outer_right", "outer_left"),
            ("inner_left", "inner_right"),
            ("inner_right", "inner_left"),
        ],
    }

    @staticmethod
    def get_mappings(axis: Axis) -> "dict[str, list]":
        axis = Axis(str(axis).lower())
        if axis == Axis.X:
            return Reflect.X
        if axis == Axis.Y:
            return Reflect.Y
        if axis == Axis.Z:
            return Reflect.Z
        raise ValueError(f"Axis not found: {axis}")


class Rotate:
    # Special logic is done elsewhere for:
    #   panes/fences/walls/etc with bool props named north/south/east/west
    #   rotations of "face" from "wall" to pick "ceiling" or "floor"
    X = {
        "axis": [
            ("y", "z"),
            ("z", "y"),
        ],
        "face": [
            ("ceiling", "wall"),
            ("floor", "wall"),
        ],
        "facing": [
            ("up", "south"),
            ("south", "down"),
            ("down", "north"),
            ("north", "up"),
        ],
        "shape": [
            ("ascending_north", "ascending_south"),
            ("ascending_south", "ascending_north"),
        ],
    }

    Y = {
        "axis": [
            ("x", "z"),
            ("z", "x"),
        ],
        "facing": [
            ("north", "west"),
            ("west", "south"),
            ("south", "east"),
            ("east", "north"),
        ],
        "rotation": [(str(r), str((r - 4) % 16)) for r in range(16)],
        "shape": [
            ("north_south", "east_west"),
            ("east_west", "north_south"),
            ("north_east", "north_west"),
            ("north_west", "south_west"),
            ("south_west", "south_east"),
            ("south_east", "north_east"),
            ("ascending_north", "ascending_west"),
            ("ascending_west", "ascending_south"),
            ("ascending_south", "ascending_east"),
            ("ascending_east", "ascending_north"),
        ],
    }

    Z = {
        "axis": [
            ("x", "y"),
            ("y", "x"),
        ],
        "face": [
            ("ceiling", "wall"),
            ("floor", "wall"),
        ],
        "facing": [
            ("up", "west"),
            ("west", "down"),
            ("down", "east"),
            ("east", "up"),
        ],
        "shape": [
            ("ascending_west", "ascending_east"),
            ("ascending_east", "ascending_west"),
        ],
    }

    @staticmethod
    def get_mappings(
        axis: Axis,
        forwards: bool = None,
        curr_face: Face = None,
        curr_facing: Direction = None,
    ) -> "dict[str, list[tuple[str,str]]]":
        axis = Axis(str(axis).lower())
        mappings = {}
        if axis == Axis.X:
            mappings = Rotate.X.copy()
            Rotate._set_face_props_x(mappings, forwards, curr_face, curr_facing)
        if axis == Axis.Y:
            mappings = Rotate.Y.copy()
        if axis == Axis.Z:
            mappings = Rotate.Z.copy()
            Rotate._set_face_props_z(mappings, forwards, curr_face, curr_facing)
        return mappings

    @staticmethod
    def _set_face_props_x(
        mappings: dict,
        forwards: bool,
        curr_face: Face,
        curr_facing: Direction,
    ) -> None:
        """Basically, gets rotations for buttons and levers."""
        if curr_face == Face.WALL:
            if curr_facing == Direction.SOUTH:
                if forwards:
                    mappings["face"] = [(curr_face, Face.CEILING)]
                else:
                    mappings["face"] = [(Face.FLOOR, curr_face)]
            elif curr_facing == Direction.NORTH:
                if forwards:
                    mappings["face"] = [(curr_face, Face.FLOOR)]
                else:
                    mappings["face"] = [(Face.CEILING, curr_face)]
        elif curr_face == Face.FLOOR:
            if forwards:
                mappings["facing"] = [(curr_facing, Direction.SOUTH)]
                mappings["face"] = [(curr_face, Face.WALL)]
            else:
                mappings["facing"] = [(Direction.NORTH, curr_facing)]
                mappings["face"] = [(Face.WALL, curr_face)]
        elif curr_face == Face.CEILING:
            if forwards:
                mappings["facing"] = [(curr_facing, Direction.NORTH)]
                mappings["face"] = [(curr_face, Face.WALL)]
            else:
                mappings["facing"] = [(Direction.SOUTH, curr_facing)]
                mappings["face"] = [(Face.WALL, curr_face)]

    @staticmethod
    def _set_face_props_z(
        mappings: dict,
        forwards: bool,
        curr_face: Face,
        curr_facing: Direction,
    ) -> None:
        """Basically, gets rotations for buttons and levers."""
        if curr_face == Face.WALL:
            if curr_facing == Direction.WEST:
                if forwards:
                    mappings["face"] = [(curr_face, Face.CEILING)]
                else:
                    mappings["face"] = [(Face.FLOOR, curr_face)]
            elif curr_facing == Direction.EAST:
                if forwards:
                    mappings["face"] = [(curr_face, Face.FLOOR)]
                else:
                    mappings["face"] = [(Face.CEILING, curr_face)]
        elif curr_face == Face.FLOOR:
            if forwards:
                mappings["facing"] = [(curr_facing, Direction.WEST)]
                mappings["face"] = [(curr_face, Face.WALL)]
            else:
                mappings["facing"] = [(Direction.EAST, curr_facing)]
                mappings["face"] = [(Face.WALL, curr_face)]
        elif curr_face == Face.CEILING:
            if forwards:
                mappings["facing"] = [(curr_facing, Direction.EAST)]
                mappings["face"] = [(curr_face, Face.WALL)]
            else:
                mappings["facing"] = [(Direction.WEST, curr_facing)]
                mappings["face"] = [(Face.WALL, curr_face)]
