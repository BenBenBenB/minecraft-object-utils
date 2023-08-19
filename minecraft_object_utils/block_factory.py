import logging
import os.path

import toml

from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class BlockProperty:
    """Describes default value and possible state values for a block property"""

    name: str
    default_state: str
    allowed_states: "list[str]"

    def __init__(
        self, name: str, default_value: str, allowed_values: "list[str]"
    ) -> None:
        self.name = name
        self.default_state = default_value
        self.allowed_states = allowed_values


class BlockTraits:
    """The definition of a block. Describes possible states and behavior in the game."""

    name: str
    properties: "list[BlockProperty]"

    def __init__(self, name: str, properties: "list[BlockProperty]" = []) -> None:
        self.name = name
        self.properties = properties

    @staticmethod
    def create_from_toml(block_name: str, block_data: dict) -> "BlockTraits":
        block_props = [
            BlockProperty(prop_name, state["default"], state["allowed"])
            for prop_name, state in (block_data.get("properties", {})).items()
        ]
        return BlockTraits(block_name, block_props)


class Block:
    """Represents a block and its state. Restricts state to valid values."""

    traits: BlockTraits
    _state: "dict[str, str]"

    @property
    def name(self) -> str:
        return self.traits.name

    def __init__(
        self,
        block_info: BlockTraits,
        initial_state: "dict[str, str]" = {},
    ) -> None:
        self.traits = block_info
        self._state = {x.name: x.default_state for x in self.traits.properties}
        for prop, value in initial_state.items():
            self.set_state(prop, value)

    def set_state(self, prop_name: str, state_value: str) -> None:
        """Sets the state of a block property."""
        block_prop = [p for p in self.traits.properties if p.name == prop_name]
        if not any(block_prop):
            raise ValueError(
                f"'{prop_name}' is not a valid property for block '{self.name}'. Valid block properties are: {[p.name for p in self.traits.properties]}"
            )
        block_prop = block_prop[0]
        if state_value in block_prop.allowed_states:
            self._state[prop_name] = state_value
        else:
            raise ValueError(
                f"'{state_value}' is not a valid state. Valid values are: {block_prop.allowed_states}"
            )

    def get_state(self, prop_name: str) -> None:
        """Gets the state for a block property."""
        return self._state.get(prop_name)


class BlockFactory:
    namespaces: "list[ModInfo]"
    blocks: "dict[str,BlockTraits]"

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.blocks = {}
        self.namespaces = []
        for mod in mods:
            self.import_namespace(mod)

    def import_namespace(self, mod: ModInfo) -> None:
        """Register a collection of blocks to factory from file."""
        imported_already = [n for n in self.namespaces if n.namespace == mod.namespace]
        if any(imported_already):
            raise ValueError(
                f"Problem importing {mod.versioned_name}. Conflict with {imported_already[0].versioned_name}"
            )
        file_path = os.path.join(mod.directory, f"{mod.versioned_name}-block.toml")
        if os.path.isfile(file_path):
            self.namespaces.append(mod)
            self.load_from_toml(file_path, mod.namespace)
        else:
            logging.warning(
                f"Skipping block import for {mod.versioned_name}. File not found: {file_path}"
            )

    def load_from_toml(self, file_path: str, namespace: str) -> None:
        """Reads block traits from toml files and stores to self.

        Args:
            file_path (str): location of file to read.
            namespace (str): namespace to save blocks under.
        """
        all_block_data: "dict[str,dict]" = toml.load(file_path)
        for block_name, block_data in all_block_data.items():
            if ":" not in block_name:
                block_name = f"{namespace}:{block_name}"
            block_info = BlockTraits.create_from_toml(block_name, block_data)
            self.register(block_info)

    def register(self, block_info: BlockTraits) -> None:
        """Saves new block traits to the factory."""
        if block_info.name in self.blocks:
            raise ValueError(f"Block '{block_info.name}' is already registered.")
        self.blocks[block_info.name] = block_info

    def create(self, block_name: str, initial_state: "dict(str,str)" = {}) -> Block:
        """Create a Block object. Optionally specify initial state.

        Args:
            block_name (str): the block's name. Example: "minecraft:dirt"
            initial_state (dict, optional): Set the block's initial state. Defaults to {}.

        Returns:
            Block: a new minecraft block
        """
        if ":" not in block_name:
            block_name = f"minecraft:{block_name}"
        if block_name in self.blocks:
            return Block(self.blocks[block_name], initial_state)
        else:
            raise ValueError(f"'{block_name}' is not registered in the BlockFactory.")
