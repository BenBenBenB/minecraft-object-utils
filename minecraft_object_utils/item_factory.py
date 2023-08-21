import logging
import os.path

import toml

from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class ItemTraits:
    """The definition of an item and common NBT tags."""

    id: str

    def __init__(self, id: str) -> None:
        self.id = id


class Item:
    """Represents an item and stores common NBT."""

    traits: ItemTraits

    @property
    def id(self) -> str:
        return self.traits.id

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
        for item_id in all_item_data:
            if ":" not in item_id:
                item_id = f"{namespace}:{item_id}"
            self.register(ItemTraits(item_id))

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
