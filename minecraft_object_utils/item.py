from .base_object import BaseObject, BaseObjectTraits
from .enchantment import Enchantment


class ItemTraits(BaseObjectTraits):
    """The definition of an item and common NBT tags."""

    max_stack_size: int
    max_damage: int
    is_fire_resistant: bool

    def __init__(self, item_id: str, **kwargs) -> None:
        super().__init__(item_id)
        self.max_stack_size = kwargs.get("max_stack_size", 64)
        self.max_damage = kwargs.get("max_damage", 0)
        self.is_fire_resistant = kwargs.get("is_fire_resistant", False)

    @staticmethod
    def create_from_toml(item_id: str, **kwargs) -> "ItemTraits":
        return ItemTraits(item_id, **kwargs)


class ItemStack(BaseObject):
    """Represents an item and stores common NBT."""

    traits: ItemTraits
    _count: int
    _damage: int
    enchantments: "list[Enchantment]"

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, new_count) -> None:
        if 1 <= new_count <= self.traits.max_stack_size:
            self._count = new_count
        else:
            raise ValueError(
                f"Count {new_count} is invalid. Max count: {self.traits.max_stack_size}"
            )

    @property
    def damage(self) -> int:
        return self._damage

    @damage.setter
    def damage(self, new_damage) -> None:
        if 0 <= new_damage <= self.traits.max_damage:
            self._damage = new_damage
        else:
            raise ValueError(
                f"Damage {new_damage} is invalid. Max damage: {self.traits.max_damage}"
            )

    def __init__(self, item_info: ItemTraits, **kwargs) -> None:
        super().__init__(item_info)
        self.count = kwargs.get("count", 1)
        self.damage = kwargs.get("damage", 0)
        self.enchantments = kwargs.get("enchantments", [])

    def __eq__(self, other: "ItemStack") -> bool:
        try:
            return (
                self.id == other.id
                and self.count == other.count
                and self.damage == other.damage
            )
        except AttributeError:
            return False
