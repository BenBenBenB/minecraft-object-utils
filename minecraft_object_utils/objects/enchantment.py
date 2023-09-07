from .base_object import BaseObject, BaseObjectTraits


class EnchantmentTraits(BaseObjectTraits):
    """The definition of an enchantment."""

    max_level: int
    category: str
    rarity: str
    curse: bool

    def __init__(self, id: str, **kwargs) -> None:
        super().__init__(id)
        self.max_level = kwargs.get("level", 1)
        self.category = kwargs.get("category", None)
        self.rarity = kwargs.get("rarity", None)
        self.curse = kwargs.get("curse", False)

    @staticmethod
    def create_from_toml(enchantment_id: str, **kwargs) -> "EnchantmentTraits":
        return EnchantmentTraits(enchantment_id, **kwargs)


class Enchantment(BaseObject):
    """Represents an enchantment."""

    traits: EnchantmentTraits
    _level: int

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, new_level) -> None:
        if 1 <= new_level <= self.traits.max_level:
            self._level = new_level
        else:
            raise ValueError(
                f"Level {new_level} is invalid. Max level: {self.traits.max_level}"
            )

    def __init__(self, enchantment_info: EnchantmentTraits, **kwargs) -> None:
        super().__init__(enchantment_info)
        self.level = kwargs.get("level", 1)
