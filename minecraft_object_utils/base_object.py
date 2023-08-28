from abc import ABC, abstractmethod


class BaseObjectTraits(ABC):
    """The definition of a minecraft object type."""

    id: str  # "namespace:object_id"

    @abstractmethod
    def __init__(self, id: str, **kwargs) -> None:
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
