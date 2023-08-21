import logging
import os.path

import toml

from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class EntityTraits:
    """The definition of an entity and common NBT tags."""

    id: str

    def __init__(self, id: str) -> None:
        self.id = id


class Entity:
    """Represents an entity and stores common NBT."""

    traits: EntityTraits

    @property
    def id(self) -> str:
        return self.traits.id

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
        for entity_id in all_entity_data:
            if ":" not in entity_id:
                entity_id = f"{namespace}:{entity_id}"
            self.register(EntityTraits(entity_id))

    def register(self, entity_info: EntityTraits) -> None:
        """Saves new entity traits to the factory."""
        if entity_info.id in self.entities:
            raise ValueError(f"Entity '{entity_info.id}' is already registered.")
        self.entities[entity_info.id] = entity_info

    def create(self, entity_id: str, initial_state: "dict(str,str)" = {}) -> Entity:
        """Create a Entity object. Optionally specify initial state.

        Args:
            entity_id (str): the entity's id. Example: "minecraft:dirt"
            initial_state (dict, optional): Set the entity's initial state. Defaults to {}.

        Returns:
            Entity: a new minecraft entity
        """
        if ":" not in entity_id:
            entity_id = f"minecraft:{entity_id}"
        if entity_id in self.entities:
            return Entity(self.entities[entity_id], initial_state)
        else:
            raise ValueError(f"'{entity_id}' is not registered in the EntityFactory.")
