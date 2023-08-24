from .base_factory import BaseObject, BaseObjectFactory, BaseObjectTraits
from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class ItemTraits(BaseObjectTraits):
    """The definition of an item and common NBT tags."""

    max_stack_size: int
    max_damage: int
    is_fire_resistant: bool

    def __init__(
        self, id: str, max_stack_size: str, max_damage, is_fire_resistant: bool
    ) -> None:
        super().__init__(id)
        self.max_stack_size = max_stack_size
        self.max_damage = max_damage
        self.is_fire_resistant = is_fire_resistant

    @staticmethod
    def create_from_toml(item_id: str, item_data: dict) -> "ItemTraits":
        return ItemTraits(
            item_id,
            item_data.get("max_stack_size", 64),
            item_data.get("max_damage", 0),
            item_data.get("is_fire_resistant", False),
        )


class ItemStack(BaseObject):
    """Represents an item and stores common NBT."""

    traits: ItemTraits
    count: int
    damage: int

    def __init__(
        self,
        item_info: ItemTraits,
        count: int = 1,
        damage: int = 0,
    ) -> None:
        super().__init__(item_info)
        self.count = count
        self.damage = damage


class ItemFactory(BaseObjectFactory):
    """Registers ItemTraits and allows creation of ItemStack instances from them."""

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self.object_type_name = "item"
        return super().__init__(mods)

    def _parse_toml(self, item_id: str, item_data: dict) -> ItemTraits:
        return ItemTraits.create_from_toml(item_id, item_data)

    def _create(self, item_id: str, initial_state: dict = {}) -> ItemStack:
        return ItemStack(
            self.registry[item_id],
            initial_state.get("count", 1),
            initial_state.get("damage", 0),
        )
