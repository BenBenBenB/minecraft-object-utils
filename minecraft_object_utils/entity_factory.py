import logging
import os.path

import toml

from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class EntityTraits:
    """The definition of an entity and common NBT tags."""

    name: str

    def __init__(self, name: str) -> None:
        self.name = name


class Entity:
    """Represents an entity and stores common NBT."""

    traits: EntityTraits

    @property
    def name(self) -> str:
        return self.traits.name

    def __init__(self, entity_info: EntityTraits) -> None:
        self.traits = entity_info


class EntityFactory:
    namespaces: "list[ModInfo]"
    entities: "dict[str,EntityTraits]"

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.entities = {}
        self.namespaces = []
        for mod in mods:
            self.import_namespace(mod)

    def import_namespace(self, mod: ModInfo) -> None:
        """Register a collection of entities to factory from file."""
        imported_already = [n for n in self.namespaces if n.namespace == mod.namespace]
        if any(imported_already):
            raise ValueError(
                f"Problem importing {mod.versioned_name}. Conflict with {imported_already[0].versioned_name}"
            )
        file_path = os.path.join(mod.directory, f"{mod.versioned_name}-entity.toml")
        if os.path.isfile(file_path):
            self.namespaces.append(mod)
            self.load_from_toml(file_path, mod.namespace)
        else:
            logging.warning(
                f"Skipping entity import for {mod.versioned_name}. File not found: {file_path}"
            )

    def load_from_toml(self, file_path: str, namespace: str) -> None:
        """Reads entity traits from toml files and stores to self.

        Args:
            file_path (str): location of file to read.
            namespace (str): namespace to save entities under.
        """
        all_entity_data: "dict[str,dict]" = toml.load(file_path)
        for entity_name in all_entity_data:
            if ":" not in entity_name:
                entity_name = f"{namespace}:{entity_name}"
            self.register(EntityTraits(entity_name))

    def register(self, entity_info: EntityTraits) -> None:
        """Saves new entity traits to the factory."""
        if entity_info.name in self.entities:
            raise ValueError(f"Entity '{entity_info.name}' is already registered.")
        self.entities[entity_info.name] = entity_info

    def create(self, entity_name: str, initial_state: "dict(str,str)" = {}) -> Entity:
        """Create a Entity object. Optionally specify initial state.

        Args:
            entity_name (str): the entity's name. Example: "minecraft:dirt"
            initial_state (dict, optional): Set the entity's initial state. Defaults to {}.

        Returns:
            Entity: a new minecraft entity
        """
        if ":" not in entity_name:
            entity_name = f"minecraft:{entity_name}"
        if entity_name in self.entities:
            return Entity(self.entities[entity_name], initial_state)
        else:
            raise ValueError(f"'{entity_name}' is not registered in the EntityFactory.")
