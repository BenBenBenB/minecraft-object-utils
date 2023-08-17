import logging
import os.path
from typing import Any

import toml
from ModInfo import VANILLA_JAVA_LATEST, ModInfo

DATA_FILE_NAME = "blocks.yaml"


class BlockState:
    _name: str
    _default_value: str
    _allowed_values: "list[str]"

    @property
    def name(self) -> str:
        return self._name

    @property
    def default_value(self) -> str:
        return self._default_value

    @property
    def allowed_values(self) -> "list(str)":
        return self._allowed_values

    def __init__(
        self, name: str, default_value: str, allowed_values: "list[str]"
    ) -> None:
        self._name = name
        self._default_value = default_value
        self._allowed_values = allowed_values


class Block:
    _name: str
    _states: "list[BlockState]"
    # nbt_tags?

    @property
    def name(self) -> str:
        return self._name

    @property
    def states(self) -> str:
        return self._states

    def __init__(
        self,
        name: str,
        states: "list[BlockState]" = [],
        initial_values: "dict(str,str)" = {},
    ) -> None:
        super().__setattr__("_name", name)
        super().__setattr__("_states", states)
        for state in states:
            super().__setattr__(state.name, state.default_value)
        for state_name, state_value in initial_values.items():
            self.__setattr__(state_name, state_value)

    def __setitem__(self, key, value) -> None:
        self.__setattr__(key, value)

    def __getitem__(self, key) -> "Block":
        return self.__getattr__(key)

    def __setattr__(self, __name: str, __value: Any) -> None:
        state = [s for s in self._states if s.name == __name]
        if not any(state):
            raise ValueError(
                f"''{__name}' is not a valid state for block '{self._name}'. Valid block states are: {[s.name for s in self.states]}"
            )
        state = state[0]
        if __value in state.allowed_values:
            super().__setattr__(__name, __value)
        else:
            raise ValueError(
                f"'{__value}' is not a valid value for '{self._name}' state '{__name}'. Valid values are: {state.allowed_values}"
            )


class BlockFactory:
    namespaces: "list[ModInfo]"
    blocks: "dict(str,list(BlockState))"

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.blocks = {}
        self.namespaces = []
        for mod in mods:
            self.import_namespace(mod)

    def import_namespace(self, mod: ModInfo) -> None:
        imported_already = [n for n in self.namespaces if n.namespace == mod.namespace]
        if any(imported_already):
            imported_name = (
                f"{imported_already[0].namespace}-{imported_already[0].version}"
            )
            raise ValueError(
                f"Skipping block import for {mod.namespace}. Already imported for same name: {imported_name}"
            )
        file_path = os.path.join(mod.directory, f"{mod.version}-block.toml")
        if os.path.isfile(file_path):
            self.namespaces.append(mod)
            self.load_from_toml(file_path, mod.namespace)
        else:
            logging.warning(
                f"Skipping block import for {mod.namespace}-{mod.version}. File not found: {file_path}"
            )

    def load_from_toml(self, file_path: str, namespace: str) -> None:
        all_block_data = toml.load(file_path)
        for block_name, block_data in all_block_data.items():
            if ":" not in block_name:
                block_name = f"{namespace}:{block_name}"
            self.blocks[block_name] = [
                BlockState(
                    state_name, state_values["default"], state_values["allowed"]
                )
                for state_name, state_values in (block_data.get("states", {})).items()
            ]

    def create(self, block_name: str, initial_values: "dict(str,str)" = {}) -> Block:
        if ":" not in block_name:
            block_name = f"minecraft:{block_name}"
        if block_name in self.blocks:
            return Block(block_name, self.blocks[block_name], initial_values)
        else:
            raise ValueError(f"'{block_name}' is not registered in the BlockFactory.")


# def __main__():
#     bf = BlockFactory()
#     nb = bf.create("note_block")
#     nb.powered = 7
#     pass

# __main__()
