import logging
import os.path
from abc import ABC
from typing import Generic, TypeVar, get_args

import toml

from .mod_info import VANILLA_JAVA_LATEST, ModInfo
from .objects.base_object import BaseObjectTraits
from .objects.block import Block, BlockTraits
from .objects.entity import Entity, EntityTraits
from .objects.item import ItemStack, ItemTraits

BObjT = TypeVar("BObjT", BlockTraits, EntityTraits, ItemTraits)
BObj = TypeVar("BObj", Block, Entity, ItemStack)


class BaseObjectFactory(ABC, Generic[BObj, BObjT]):
    """Stores collection of BaseObjectTraits and allows you to create instances of BaseObject from them."""

    imported: "list[str]"
    mods: "list[ModInfo]"
    registry: "dict[str,BObjT]"
    file_name_part: str  # block, item, or entity
    BaseObjType: BObj
    BaseObjTraitType: BObjT

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.registry = {}
        self.mods = []
        self.imported = []

        types = get_args(self.__orig_bases__[0])
        self.BaseObjType = types[0]
        self.BaseObjTraitType = types[1]

        for mod in mods:
            self.import_mod(mod)

    def import_mod(self, mod: ModInfo) -> None:
        """Register a collection of object traits to factory from file."""
        file_path = mod.get_file_path(self.file_name_part)
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
                object_traits = self.BaseObjTraitType.create_from_toml(
                    object_id, **object_data
                )
                self.register(object_traits)
        self.imported.append(file_path)
        return True

    def register(self, object_traits: BaseObjectTraits) -> None:
        """Saves new traits to the factory."""
        if object_traits.id in self.registry:
            raise ValueError(
                f"Already registered {self.file_name_part} {object_traits.id}"
            )
        self.registry[object_traits.id] = object_traits

    def create(self, object_id: str, **kwargs) -> BObj:
        """Create a BaseObject derived object. Optionally specify initial state.

        Args:
            object_id (str): the object's id. Example: "minecraft:dirt"
            **kwargs: Use keyword arguments to set the object's initial state.

        Returns:
            BaseObject: a new instance of BaseObjType
        """
        if ":" not in object_id:
            object_id = f"minecraft:{object_id}"
        if object_id in self.registry:
            return self.BaseObjType(self.registry[object_id], **kwargs)
        else:
            raise ValueError(f"{self.__class__.__name__} has no {object_id}.")
