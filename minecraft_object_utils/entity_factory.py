from .base_factory import BaseObject, BaseObjectFactory, BaseObjectTraits
from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class EntityTraits(BaseObjectTraits):
    """The definition of an entity and common NBT tags."""

    def __init__(self, id: str) -> None:
        super().__init__(id)

    @staticmethod
    def create_from_toml(entity_id: str, entity_data: dict) -> "EntityTraits":
        return EntityTraits(entity_id)


class Entity(BaseObject):
    """Represents an entity and stores common NBT."""

    traits: EntityTraits

    def __init__(self, entity_info: EntityTraits, initial_state: dict) -> None:
        super().__init__(entity_info)


class EntityFactory(BaseObjectFactory):
    """Registers EntityTraits and allows creation of Entity instances from them."""

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.object_type_name = "entity"
        return super().__init__(mods)

    def _parse_toml(self, entity_id: str, item_data: dict) -> BaseObjectTraits:
        return EntityTraits.create_from_toml(entity_id, item_data)

    def _create(self, entity_id: str, initial_state: dict) -> Entity:
        return Entity(self.registry[entity_id], initial_state)
