from .base_factory import BaseObject, BaseObjectFactory, BaseObjectTraits
from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class ItemTraits(BaseObjectTraits):
    """The definition of an item and common NBT tags."""

    def __init__(self, id: str) -> None:
        super().__init__(id)

    @staticmethod
    def create_from_toml(item_id: str, item_data: dict) -> "ItemTraits":
        return ItemTraits(item_id)


class Item(BaseObject):
    """Represents an item and stores common NBT."""

    traits: ItemTraits

    def __init__(self, item_info: ItemTraits, initial_state: dict) -> None:
        super().__init__(item_info)


class ItemFactory(BaseObjectFactory):
    """Registers ItemTraits and allows creation of Item instances from them."""

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.object_type_name = "item"
        return super().__init__(mods)

    def _parse_toml(self, item_id: str, item_data: dict) -> ItemTraits:
        return ItemTraits.create_from_toml(item_id, item_data)

    def _create(self, item_id: str, initial_state: dict) -> Item:
        return Item(self.registry[item_id], initial_state)
