import logging
import os.path

import toml

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


class BlockTraits:
    """The definition of a block. Describes possible states and behavior in the game."""

    id: str
    properties: "list[BlockProperty]"

    def __init__(self, id: str, properties: "list[BlockProperty]" = []) -> None:
        self.id = id
        self.properties = properties

    @staticmethod
    def create_from_toml(block_id: str, block_data: dict) -> "BlockTraits":
        block_props = [
            BlockProperty(prop_name, state["default"], state["allowed"])
            for prop_name, state in (block_data.get("properties", {})).items()
        ]
        return BlockTraits(block_id, block_props)


class Block:
    """Represents a block and its state. Restricts state to valid values."""

    traits: BlockTraits
    _state: "dict[str, str]"

    @property
    def id(self) -> str:
        return self.traits.id

    def __init__(
        self,
        block_info: BlockTraits,
        initial_state: "dict[str, str]" = {},
    ) -> None:
        self.traits = block_info
        self._state = {x.id: x.default for x in self.traits.properties}
        for prop, value in initial_state.items():
            self.set_state(prop, value)

    def set_state(self, prop_name: str, state_value: str) -> None:
        """Sets the state of a block property."""
        prop_name = str(prop_name).lower()
        block_prop = [p for p in self.traits.properties if p.id == prop_name]
        if not any(block_prop):
            raise ValueError(
                f"'{prop_name}' is not a valid property for block '{self.id}'. Valid block properties are: {[p.id for p in self.traits.properties]}"
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


class BlockFactory:
    """Stores collection of BlockTraits and allows you to create instances of Block from them."""

    imported: "list[str]"
    mods: "list[ModInfo]"
    blocks: "dict[str,BlockTraits]"

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.blocks = {}
        self.mods = []
        self.imported = []
        for mod in mods:
            self.import_mod(mod)

    def import_mod(self, mod: ModInfo) -> None:
        """Register a collection of blocks to factory from file."""
        file_path = mod.get_file_path("block")
        if os.path.isfile(file_path):
            self.mods.append(mod)
            self.load_from_toml(file_path)
        else:
            logging.warning(
                f"Skipping block import for {mod.versioned_name}. File not found: {file_path}"
            )

    def load_from_toml(self, file_path: str) -> None:
        """Reads block traits from toml files and stores to self.

        Args:
            file_path (str): location of file to read.
        """
        if file_path in self.imported:
            logging.warning(f"Skipping import. Already loaded file: {file_path}")
            return
        all_block_data: "dict[str,dict]" = toml.load(file_path)
        for namespace, namespace_blocks in all_block_data.items():
            for block_id, block_data in namespace_blocks.items():
                if ":" not in block_id:
                    block_id = f"{namespace}:{block_id}"
                block_info = BlockTraits.create_from_toml(block_id, block_data)
                self.register(block_info)
        self.imported.append(file_path)

    def register(self, block_info: BlockTraits) -> None:
        """Saves new block traits to the factory."""
        if block_info.id in self.blocks:
            raise ValueError(f"Block '{block_info.id}' is already registered.")
        self.blocks[block_info.id] = block_info

    def create(self, block_id: str, initial_state: "dict(str,str)" = {}) -> Block:
        """Create a Block object. Optionally specify initial state.

        Args:
            block_id (str): the block's id. Example: "minecraft:dirt"
            initial_state (dict, optional): Set the block's initial state. Defaults to {}.

        Returns:
            Block: a new minecraft block
        """
        if ":" not in block_id:
            block_id = f"minecraft:{block_id}"
        if block_id in self.blocks:
            return Block(self.blocks[block_id], initial_state)
        else:
            raise ValueError(f"'{block_id}' is not registered in the BlockFactory.")
