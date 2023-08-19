import logging
import os.path

import toml

from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class ItemTraits:
    """The definition of an item and common NBT tags."""

    name: str

    def __init__(self, name: str) -> None:
        self.name = name


class Item:
    """Represents an item and stores common NBT."""

    traits: ItemTraits

    @property
    def name(self) -> str:
        return self.traits.name

    def __init__(self, item_info: ItemTraits) -> None:
        self.traits = item_info


class ItemFactory:
    namespaces: "list[ModInfo]"
    items: "dict[str,ItemTraits]"

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.items = {}
        self.namespaces = []
        for mod in mods:
            self.import_namespace(mod)

    def import_namespace(self, mod: ModInfo) -> None:
        """Register a collection of items to factory from file."""
        imported_already = [n for n in self.namespaces if n.namespace == mod.namespace]
        if any(imported_already):
            raise ValueError(
                f"Problem importing {mod.versioned_name}. Conflict with {imported_already[0].versioned_name}"
            )
        file_path = os.path.join(mod.directory, f"{mod.versioned_name}-item.toml")
        if os.path.isfile(file_path):
            self.namespaces.append(mod)
            self.load_from_toml(file_path, mod.namespace)
        else:
            logging.warning(
                f"Skipping item import for {mod.versioned_name}. File not found: {file_path}"
            )

    def load_from_toml(self, file_path: str, namespace: str) -> None:
        """Reads item traits from toml files and stores to self.

        Args:
            file_path (str): location of file to read.
            namespace (str): namespace to save items under.
        """
        all_item_data: "dict[str,dict]" = toml.load(file_path)
        for item_name in all_item_data:
            if ":" not in item_name:
                item_name = f"{namespace}:{item_name}"
            self.register(ItemTraits(item_name))

    def register(self, item_info: ItemTraits) -> None:
        """Saves new item traits to the factory."""
        if item_info.name in self.items:
            raise ValueError(f"Item '{item_info.name}' is already registered.")
        self.items[item_info.name] = item_info

    def create(self, item_name: str, initial_state: "dict(str,str)" = {}) -> Item:
        """Create a Item object. Optionally specify initial state.

        Args:
            item_name (str): the item's name. Example: "minecraft:dirt"
            initial_state (dict, optional): Set the item's initial state. Defaults to {}.

        Returns:
            Item: a new minecraft item
        """
        if ":" not in item_name:
            item_name = f"minecraft:{item_name}"
        if item_name in self.items:
            return Item(self.items[item_name], initial_state)
        else:
            raise ValueError(f"'{item_name}' is not registered in the ItemFactory.")
