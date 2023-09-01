from .base_object import BaseObject, BaseObjectTraits
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

    def __init__(self, traits: BlockTraits, **kwargs) -> None:
        super().__init__(traits)
        if self.traits.inventory_slots is not None:
            self.inventory = Inventory(self.traits.inventory_slots)

        self._state = {x.id: x.default for x in self.traits.props}
        for prop, value in kwargs.items():
            self.set_state(prop, value)

    def set_state(self, prop_name: str, state_value: str) -> None:
        """Sets the state of a block property."""
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

    def get_state(self, prop_name: str) -> str:
        """Gets the state for a block property."""
        prop_name = str(prop_name).lower()
        return self._state.get(prop_name)
