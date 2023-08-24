from .base_factory import BaseObject, BaseObjectFactory, BaseObjectTraits


class EntityTraits(BaseObjectTraits):
    """The definition of an entity and common NBT tags."""

    category: str
    width: float
    height: float
    fire_immune: bool

    def __init__(
        self, id: str, category: str, width: float, height: float, fire_immune: bool
    ) -> None:
        super().__init__(id)
        self.category = category
        self.width = width
        self.height = height
        self.fire_immune = fire_immune

    @staticmethod
    def create_from_toml(entity_id: str, entity_data: dict) -> "EntityTraits":
        return EntityTraits(
            entity_id,
            entity_data.get("category", "MISC"),
            entity_data.get("width", 0),
            entity_data.get("height", 0),
            entity_data.get("fire_immune", False),
        )


class Entity(BaseObject):
    """Represents an entity and stores common NBT."""

    traits: EntityTraits

    def __init__(self, entity_info: EntityTraits, initial_state: dict) -> None:
        super().__init__(entity_info)


class EntityFactory(BaseObjectFactory[Entity, EntityTraits]):
    """Registers EntityTraits and allows creation of Entity instances from them."""

    file_name_part: str = "entity"
    BaseObjType: type = Entity
    BaseObjTraitType: type = EntityTraits
