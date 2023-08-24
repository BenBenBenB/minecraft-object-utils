from .base_factory import BaseObject, BaseObjectFactory, BaseObjectTraits


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
    _count: int
    _damage: int

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

    def __init__(
        self, item_info: ItemTraits, initial_state: "dict[str, str]" = {}
    ) -> None:
        super().__init__(item_info)
        self.count = initial_state.get("count", 1)
        self.damage = initial_state.get("damage", 0)


class ItemFactory(BaseObjectFactory[ItemStack, ItemTraits]):
    """Registers ItemTraits and allows creation of ItemStack instances from them."""

    file_name_part: str = "item"
    BaseObjType: type = ItemStack
    BaseObjTraitType: type = ItemTraits
