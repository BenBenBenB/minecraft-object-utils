import logging
import os.path

import toml

from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class EntityTraits:
    """The definition of an entity and common NBT tags."""

    id: str

    def __init__(self, id: str) -> None:
        self.id = id

    @staticmethod
    def create_from_toml(entity_id: str, entity_data: dict) -> "EntityTraits":
        return EntityTraits(entity_id)


class Entity:
    """Represents an entity and stores common NBT."""

    traits: EntityTraits

    @property
    def id(self) -> str:
        return self.traits.id

    def __init__(self, entity_info: EntityTraits) -> None:
        self.traits = entity_info


class EntityFactory:
    """Stores collection of BlockTraits and allows you to create instances of Item from them."""

    imported: "list[str]"
    mods: "list[ModInfo]"
    entities: "dict[str,EntityTraits]"

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.entities = {}
        self.mods = []
        self.imported = []
        for mod in mods:
            self.import_mod(mod)

    def import_mod(self, mod: ModInfo) -> None:
        """Register a collection of entities to factory from file."""
        file_path = mod.get_file_path("entity")
        if os.path.isfile(file_path):
            self.mods.append(mod)
            self.load_from_toml(file_path)
        else:
            logging.warning(
                f"Skipping entity import for {mod.versioned_name}. File not found: {file_path}"
            )

    def load_from_toml(self, file_path: str) -> None:
        """Reads entity traits from toml files and stores to self.

        Args:
            file_path (str): location of file to read.
        """
        if file_path in self.imported:
            logging.warning(f"Skipping import. Already loaded file: {file_path}")
            return
        all_entity_data: "dict[str,dict]" = toml.load(file_path)
        for namespace, namespace_entities in all_entity_data.items():
            for entity_id, entity_data in namespace_entities.items():
                if ":" not in entity_id:
                    entity_id = f"{namespace}:{entity_id}"
                entity_info = EntityTraits.create_from_toml(entity_id, entity_data)
                self.register(entity_info)
        self.imported.append(file_path)

    def register(self, entity_info: EntityTraits) -> None:
        """Saves new entity traits to the factory."""
        if entity_info.id in self.entities:
            raise ValueError(f"Entity '{entity_info.id}' is already registered.")
        self.entities[entity_info.id] = entity_info

    def create(self, entity_id: str) -> Entity:
        """Create a Entity object. Optionally specify initial state.

        Args:
            entity_id (str): the entity's id. Example: "minecraft:cow"

        Returns:
            Entity: a new minecraft entity
        """
        if ":" not in entity_id:
            entity_id = f"minecraft:{entity_id}"
        if entity_id in self.entities:
            return Entity(self.entities[entity_id])
        else:
            raise ValueError(f"'{entity_id}' is not registered in the EntityFactory.")
