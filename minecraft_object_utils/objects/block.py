import contextlib

from .base_object import BaseObject, BaseObjectTraits
from .block_state.constants import Axis, Direction
from .block_state.transformations import Reflect, Rotate
from .inventory import Inventory


class BlockProperty:
    """Describes default value and possible state values for a block property"""

    id: str
    default: str
    allowed: "list[str]"

    def __init__(
        self, id: str, default_value: str, allowed_values: "list[str]"
    ) -> None:
        self.id = id
        self.default = str(default_value).lower()
        self.allowed = [str(v).lower() for v in allowed_values]


class BlockTraits(BaseObjectTraits):
    """The definition of a block. Describes possible states and behavior in the game."""

    props: "list[BlockProperty]"
    piston_behavior: str
    inventory_slots: int

    def __init__(self, id: str, **kwargs) -> None:
        super().__init__(id)
        self.props = kwargs.get("props", [])
        self.inventory_slots = kwargs.get("inventory_slots", None)
        self.piston_behavior = kwargs.get("piston_behavior", "NORMAL")

    @staticmethod
    def create_from_toml(block_id: str, **kwargs: dict) -> "BlockTraits":
        prop_dict = kwargs.get("properties", {})
        piston_behavior = kwargs.get("piston_behavior", "NORMAL")
        inventory_slots = kwargs.get("inventory_slots", None)

        block_props = [
            BlockProperty(prop_name, state["default"], state["allowed"])
            for prop_name, state in prop_dict.items()
        ]
        return BlockTraits(
            block_id,
            props=block_props,
            piston_behavior=piston_behavior,
            inventory_slots=inventory_slots,
        )


class Block(BaseObject):
    """Represents a block and its state. Restricts state to valid values."""

    _state: "dict[str, str]"
    traits: BlockTraits
    inventory: Inventory

    @property
    def state(self) -> "dict[str, str]":
        """Gets a copy of the block's state."""
        return self._state.copy()

    def __init__(self, traits: BlockTraits, **kwargs) -> None:
        super().__init__(traits)
        if self.traits.inventory_slots is not None:
            self.inventory = Inventory(self.traits.inventory_slots)

        self._state = {x.id: x.default for x in self.traits.props}
        self.set_states(**kwargs)

    def copy(self) -> "Block":
        return Block(self.traits, **self._state)

    def set_state(self, prop_name: str, state_value: str) -> None:
        """Sets the state of a block property.

        Args:
            prop_name (str): the name of the property
            state_value (str): the value to be set"""
        prop_name = str(prop_name).lower()
        block_prop = [p for p in self.traits.props if p.id == prop_name]
        if not any(block_prop):
            raise ValueError(
                f"'{prop_name}' is not a valid property for block {self.id}. Valid properties are: {[p.id for p in self.traits.props]}"
            )
        block_prop = block_prop[0]
        state_value = str(state_value).lower()
        if state_value in block_prop.allowed:
            self._state[prop_name] = state_value
        else:
            raise ValueError(
                f"'{state_value}' is not a valid state. Valid values are: {block_prop.allowed}"
            )

    def set_states(self, **kwargs) -> None:
        """Sets the states of input block property keyword arguments."""
        for prop, value in kwargs.items():
            self.set_state(prop, value)

    def get_state(self, prop_name: str) -> str:
        """Gets the state for a block property.

        Args:
            prop_name (str): the name of the property"""
        prop_name = str(prop_name).lower()
        return self._state.get(prop_name)

    def try_get_state(self, prop_name: str, default: any) -> str:
        """Gets the state for a block property. Return default if not found.

        Args:
            prop_name (str): the name of the property
            default (any): Value to return if block does not have property"""
        prop_name = str(prop_name).lower()
        return self._state.get(prop_name, default)

    def reflect(self, axis: Axis) -> None:
        """Update block state to swap north & south (x), up & down (y), or east & west (z).

        Args:
            axis (Axis): x, y, or z. Flip states along this direction.

        Some blocks do not have true reflections over the y-axis. Beware of:
            rail, torch, banner, carpet, pressure plate, bed, plants, etc.
        """
        axis = Axis(str(axis).lower())
        if not any(self._state):
            return
        self._reflect_props(axis)
        self._reflect_compass_props(axis)

    def rotate(self, axis: Axis, angle: int) -> None:
        """Rotates block about axis by angle.

        Args:
            axis (Axis): x, y, or z. Rotate blocks about this axis.
            angle (int): A multiple of 90

        Some blocks can't truly rotate states for x and z axis rotations of 90 or 270 degrees:
            Beware of banners, doors, torches, rails. slabs, fences, stairs, dripstone, plants, etc.

        Rotation follows the "right hand rule". To visualize:
            Point your right thumb along the positive direction of axis with fingers outstretched. Curl your fingers toward your palm.
            They will naturally curl in the same direction the block will rotate for postitive angles.

        Example:
            If axis is Y and angle is 90, when you look up at the block from below (facing +y), it will appear to rotate clockwise 90 degrees.
        """
        axis = Axis(str(axis).lower())
        angle = angle % 360
        if angle not in [90, 180, 270]:
            raise ValueError("Rotation angle must correspond to 90, 180, or 270")

        if not any(self._state):
            return

        if angle == 180:
            # two reflections are equivalent to a 180 degree rotation.
            for reflection_axis in Axis:
                if axis != reflection_axis:
                    self.reflect(reflection_axis)
        else:
            forwards = angle == 90
            self._rotate_props_90(axis, forwards)
            self._rotate_direction_props_90(axis, forwards)

    def _reflect_props(self, axis: Axis) -> None:
        "Update state from predefined list of reflection mappings."
        source, target = 0, 1

        if axis == Axis.X:
            prop_maps = Reflect.X
        if axis == Axis.Y:
            prop_maps = Reflect.Y
        if axis == Axis.Z:
            prop_maps = Reflect.Z

        for state_name, curr_value in self._state.items():
            if state_name in prop_maps:
                new_value = next(
                    (
                        m[target]
                        for m in prop_maps[state_name]
                        if m[source] == curr_value
                    ),
                    None,
                )
                if new_value is not None:
                    # Some states may not be reflectable .
                    # Attempt the state change and ignore failure.
                    with contextlib.suppress(ValueError):
                        self.set_state(state_name, new_value)

    def _reflect_compass_props(self, axis: Axis) -> None:
        "Swap prop pairs: (east, west),(up, down),(north, south)"
        if (
            axis == Axis.X
            and Direction.EAST in self._state
            and Direction.WEST in self._state
        ):
            self._state[Direction.EAST], self._state[Direction.WEST] = (
                self._state[Direction.WEST],
                self._state[Direction.EAST],
            )
        if (
            axis == Axis.Y
            and Direction.UP in self._state
            and Direction.DOWN in self._state
        ):
            self._state[Direction.UP], self._state[Direction.DOWN] = (
                self._state[Direction.DOWN],
                self._state[Direction.UP],
            )
        if (
            axis == Axis.Z
            and Direction.NORTH in self._state
            and Direction.SOUTH in self._state
        ):
            self._state[Direction.NORTH], self._state[Direction.SOUTH] = (
                self._state[Direction.SOUTH],
                self._state[Direction.NORTH],
            )

    def _rotate_props_90(self, axis: Axis, forwards: bool) -> None:
        "Update props from predefined list of rotation mappings."
        if forwards:
            source, target = 0, 1
        else:
            source, target = 1, 0

        prop_maps = Rotate.get_mappings(
            axis,
            forwards,
            self.try_get_state("face", None),
            self.try_get_state("facing", None),
        )

        for state_name, curr_value in self._state.items():
            if state_name in prop_maps:
                new_value = next(
                    (
                        m[target]
                        for m in prop_maps[state_name]
                        if m[source] == curr_value
                    ),
                    None,
                )
                if new_value is not None:
                    # Some states may not be rotatable.
                    # Attempt the state change and ignore failure.
                    with contextlib.suppress(ValueError):
                        self.set_state(state_name, new_value)

    def _rotate_direction_props_90(self, axis: Axis, forwards: bool) -> None:
        "Rotate props with name: up, down, north, south, east, west"
        if axis == Axis.X:
            self._rotate_direction_props_90_x(forwards)
        if axis == Axis.Y:
            self._rotate_direction_props_90_y(forwards)
        if axis == Axis.Z:
            self._rotate_direction_props_90_z(forwards)

    def _rotate_direction_props_90_x(self, forwards: bool) -> None:
        "Rotate props: up, south, down, north"
        if not all(
            state_name in self._state
            for state_name in [
                Direction.UP,
                Direction.SOUTH,
                Direction.DOWN,
                Direction.NORTH,
            ]
        ):
            return
        if forwards:
            (
                self._state[Direction.SOUTH],
                self._state[Direction.DOWN],
                self._state[Direction.NORTH],
                self._state[Direction.UP],
            ) = (
                self._state[Direction.UP],
                self._state[Direction.SOUTH],
                self._state[Direction.DOWN],
                self._state[Direction.NORTH],
            )
        else:
            (
                self._state[Direction.NORTH],
                self._state[Direction.UP],
                self._state[Direction.SOUTH],
                self._state[Direction.DOWN],
            ) = (
                self._state[Direction.UP],
                self._state[Direction.SOUTH],
                self._state[Direction.DOWN],
                self._state[Direction.NORTH],
            )

    def _rotate_direction_props_90_y(self, forwards: bool) -> None:
        "Rotate props: north, west, south, east"
        if not all(
            state_name in self._state
            for state_name in [
                Direction.NORTH,
                Direction.WEST,
                Direction.SOUTH,
                Direction.EAST,
            ]
        ):
            return
        if forwards:
            (
                self._state[Direction.WEST],
                self._state[Direction.NORTH],
                self._state[Direction.EAST],
                self._state[Direction.SOUTH],
            ) = (
                self._state[Direction.NORTH],
                self._state[Direction.EAST],
                self._state[Direction.SOUTH],
                self._state[Direction.WEST],
            )
        else:
            (
                self._state[Direction.EAST],
                self._state[Direction.SOUTH],
                self._state[Direction.WEST],
                self._state[Direction.NORTH],
            ) = (
                self._state[Direction.NORTH],
                self._state[Direction.EAST],
                self._state[Direction.SOUTH],
                self._state[Direction.WEST],
            )

    def _rotate_direction_props_90_z(self, forwards: bool) -> None:
        "Rotate props: up, west, down, east"
        if not all(
            state_name in self._state
            for state_name in [
                Direction.UP,
                Direction.WEST,
                Direction.DOWN,
                Direction.EAST,
            ]
        ):
            return
        if forwards:
            (
                self._state[Direction.WEST],
                self._state[Direction.DOWN],
                self._state[Direction.EAST],
                self._state[Direction.UP],
            ) = (
                self._state[Direction.UP],
                self._state[Direction.WEST],
                self._state[Direction.DOWN],
                self._state[Direction.EAST],
            )
        else:
            (
                self._state[Direction.EAST],
                self._state[Direction.UP],
                self._state[Direction.WEST],
                self._state[Direction.DOWN],
            ) = (
                self._state[Direction.UP],
                self._state[Direction.WEST],
                self._state[Direction.DOWN],
                self._state[Direction.EAST],
            )
