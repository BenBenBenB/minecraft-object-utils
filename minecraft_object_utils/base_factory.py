import logging
import os.path
from abc import ABC, abstractmethod

import toml

from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class BaseObjectTraits(ABC):
    """The definition of a minecraft object type."""

    id: str

    @abstractmethod
    def __init__(self, id: str) -> None:
        self.id = id

    @staticmethod
    @abstractmethod
    def create_from_toml(object_id: str, item_data: dict) -> "BaseObjectTraits":
        return BaseObjectTraits(object_id)


class BaseObject(ABC):
    """Represents a minecraft object, and its characteristics, and its state."""

    traits: BaseObjectTraits

    @property
    def id(self) -> str:
        return self.traits.id

    @abstractmethod
    def __init__(self, object_info: BaseObjectTraits) -> None:
        self.traits = object_info


class BaseObjectFactory(ABC):
    """Stores collection of BaseObjectTraits and allows you to create instances of BaseObject from them."""

    imported: "list[str]"
    mods: "list[ModInfo]"
    registry: "dict[str,BaseObjectTraits]"
    object_type_name: str

    @abstractmethod
    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.registry = {}
        self.mods = []
        self.imported = []
        for mod in mods:
            self.import_mod(mod)

    def import_mod(self, mod: ModInfo) -> None:
        """Register a collection of object traits to factory from file."""
        file_path = mod.get_file_path(self.object_type_name)
        if self.load_from_toml(file_path):
            self.mods.append(mod)

    def load_from_toml(self, file_path: str) -> bool:
        """Reads object traits from toml files and stores to self.

        Args:
            file_path (str): location of file to read.

        Returns:
            bool: true if the file imported, otherwise false.
        """
        if not os.path.isfile(file_path):
            logging.warning(f"Skipping import. File not found: {file_path}")
            return False
        if file_path in self.imported:
            logging.warning(f"Skipping import. Already loaded file: {file_path}")
            return False
        all_object_data: "dict[str,dict]" = toml.load(file_path)
        for namespace, namespace_traits in all_object_data.items():
            for object_id, object_data in namespace_traits.items():
                if ":" not in object_id:
                    object_id = f"{namespace}:{object_id}"
                object_traits = self._parse_toml(object_id, object_data)
                self.register(object_traits)
        self.imported.append(file_path)
        return True

    @abstractmethod
    def _parse_toml(self, object_id: str, item_data: dict) -> BaseObjectTraits:
        return BaseObjectTraits.create_from_toml(object_id, item_data)

    def register(self, object_traits: BaseObjectTraits) -> None:
        """Saves new traits to the factory."""
        if object_traits.id in self.registry:
            raise ValueError(
                f"Already registered {self.object_type_name} {object_traits.id}"
            )
        self.registry[object_traits.id] = object_traits

    def create(self, object_id: str, initial_state: "dict(str,str)" = {}) -> BaseObject:
        """Create a BaseObject object. Optionally specify initial state.

        Args:
            object_id (str): the object's id. Example: "minecraft:dirt"
            initial_state (dict, optional): Set the object's initial state. Defaults to {}.

        Returns:
            BaseObject: a new minecraft object
        """
        if ":" not in object_id:
            object_id = f"minecraft:{object_id}"
        if object_id in self.registry:
            return self._create(object_id, initial_state)
        else:
            raise ValueError(f"{self.__class__.__name__} has no {object_id}.")

    @abstractmethod
    def _create(
        self, object_id: str, initial_state: "dict(str,str)" = {}
    ) -> BaseObject:
        return BaseObject(self.registry[object_id], initial_state)
