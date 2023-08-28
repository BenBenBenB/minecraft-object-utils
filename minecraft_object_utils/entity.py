from .base_object import BaseObject, BaseObjectTraits


class EntityTraits(BaseObjectTraits):
    """The definition of an entity and common NBT tags."""

    category: str
    width: float
    height: float
    fire_immune: bool

    def __init__(self, id: str, **kwargs) -> None:
        super().__init__(id)
        self.category = kwargs.get("category", "MISC")
        self.width = kwargs.get("width", 0.0)
        self.height = kwargs.get("height", 0.0)
        self.fire_immune = kwargs.get("fire_immune", False)

    @staticmethod
    def create_from_toml(entity_id: str, **kwargs) -> "EntityTraits":
        return EntityTraits(entity_id, **kwargs)


class Entity(BaseObject):
    """Represents an entity and stores common NBT."""

    traits: EntityTraits

    def __init__(self, entity_info: EntityTraits, **kwargs) -> None:
        super().__init__(entity_info)
