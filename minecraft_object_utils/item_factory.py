import logging
import os.path

import toml

from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class ItemTraits:
    """The definition of an item and common NBT tags."""

    id: str

    def __init__(self, id: str) -> None:
        self.id = id

    @staticmethod
    def create_from_toml(item_id: str, item_data: dict) -> "ItemTraits":
        return ItemTraits(item_id)


class Item:
    """Represents an item and stores common NBT."""

    traits: ItemTraits

    @property
    def id(self) -> str:
        return self.traits.id

    def __init__(self, item_info: ItemTraits) -> None:
        self.traits = item_info


class ItemFactory:
    """Stores collection of ItemTraits and allows you to create instances of Item from them."""

    imported: "list[str]"
    mods: "list[ModInfo]"
    items: "dict[str,ItemTraits]"

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.items = {}
        self.mods = []
        self.imported = []
        for mod in mods:
            self.import_mod(mod)

    def import_mod(self, mod: ModInfo) -> None:
        """Register a collection of items to factory from file."""
        file_path = mod.get_file_path("item")
        if os.path.isfile(file_path):
            self.mods.append(mod)
            self.load_from_toml(file_path)
        else:
            logging.warning(
                f"Skipping item import for {mod.versioned_name}. File not found: {file_path}"
            )

    def load_from_toml(self, file_path: str) -> None:
        """Reads item traits from toml files and stores to self.

        Args:
            file_path (str): location of file to read.
        """
        if file_path in self.imported:
            logging.warning(f"Skipping import. Already loaded file: {file_path}")
            return
        all_item_data: "dict[str,dict]" = toml.load(file_path)
        for namespace, namespace_items in all_item_data.items():
            for item_id, item_data in namespace_items.items():
                if ":" not in item_id:
                    item_id = f"{namespace}:{item_id}"
                item_info = ItemTraits.create_from_toml(item_id, item_data)
                self.register(item_info)
        self.imported.append(file_path)

    def register(self, item_info: ItemTraits) -> None:
        """Saves new item traits to the factory."""
        if item_info.id in self.items:
            raise ValueError(f"Item '{item_info.id}' is already registered.")
        self.items[item_info.id] = item_info

    def create(self, item_id: str, initial_state: "dict(str,str)" = {}) -> Item:
        """Create a Item object. Optionally specify initial state.

        Args:
            item_id (str): the item's id. Example: "minecraft:dirt"
            initial_state (dict, optional): Set the item's initial state. Defaults to {}.

        Returns:
            Item: a new minecraft item
        """
        if ":" not in item_id:
            item_id = f"minecraft:{item_id}"
        if item_id in self.items:
            return Item(self.items[item_id], initial_state)
        else:
            raise ValueError(f"'{item_id}' is not registered in the ItemFactory.")
