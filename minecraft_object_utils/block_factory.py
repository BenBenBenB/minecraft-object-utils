from .base_factory import BaseObject, BaseObjectFactory, BaseObjectTraits
from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class BlockProperty:
    """Describes default value and possible state values for a block property"""

    id: str
    default: str
    allowed: "list[str]"

    def __init__(
        self, id: str, default_value: str, allowed_values: "list[str]"
    ) -> None:
        self.id = id
        self.default = default_value
        self.allowed = allowed_values

    @staticmethod
    def create_list_from_toml(block_props: dict) -> "BlockTraits":
        return [
            BlockProperty(prop_name, state["default"], state["allowed"])
            for prop_name, state in block_props.items()
        ]


class BlockTraits(BaseObjectTraits):
    """The definition of a block. Describes possible states and behavior in the game."""

    props: "list[BlockProperty]"

    def __init__(
        self,
        id: str,
        piston_behavior: str,
        props: "list[BlockProperty]" = [],
    ) -> None:
        super().__init__(id)
        self.props = props
        self.piston_behavior = piston_behavior

    @staticmethod
    def create_from_toml(block_id: str, block_data: dict) -> "BlockTraits":
        block_props = BlockProperty.create_list_from_toml(
            block_data.get("properties", {})
        )
        return BlockTraits(
            block_id,
            block_data.get("piston_behavior", "NORMAL"),
            block_props,
        )


class Block(BaseObject):
    """Represents a block and its state. Restricts state to valid values."""

    _state: "dict[str, str]"
    traits: BlockTraits

    def __init__(
        self, traits: BlockTraits, initial_state: "dict[str, str]" = {}
    ) -> None:
        super().__init__(traits)
        self._state = {x.id: x.default for x in self.traits.props}
        for prop, value in initial_state.items():
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

    def get_state(self, prop_name: str) -> None:
        """Gets the state for a block property."""
        prop_name = str(prop_name).lower()
        return self._state.get(prop_name)


class BlockFactory(BaseObjectFactory):
    """Registers BlockTraits and allows creation of Block instances from them."""

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.object_type_name = "block"
        return super().__init__(mods)

    def _parse_toml(self, entity_id: str, item_data: dict) -> BlockTraits:
        return BlockTraits.create_from_toml(entity_id, item_data)

    def _create(self, block_id: str, initial_state: "dict(str,str)" = {}) -> Block:
        return Block(self.registry[block_id], initial_state)
