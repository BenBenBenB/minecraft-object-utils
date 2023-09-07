from .base_factory import BaseObjectFactory
from .mod_info import VANILLA_JAVA_LATEST, ModInfo
from .objects.block import Block, BlockTraits
from .objects.enchantment import Enchantment, EnchantmentTraits
from .objects.entity import Entity, EntityTraits
from .objects.item import ItemStack, ItemTraits


class BlockFactory(BaseObjectFactory[Block, BlockTraits]):
    """Registers BlockTraits and allows creation of Block instances from them."""

    file_name_part: str = "block"


class EnchantmentFactory(BaseObjectFactory[Enchantment, EnchantmentTraits]):
    """Registers EnchantmentTraits and allows creation of Enchantment instances from them."""

    file_name_part: str = "enchantment"


class EntityFactory(BaseObjectFactory[Entity, EntityTraits]):
    """Registers EntityTraits and allows creation of Entity instances from them."""

    file_name_part: str = "entity"


class ItemFactory(BaseObjectFactory[ItemStack, ItemTraits]):
    """Registers ItemTraits and allows creation of ItemStack instances from them."""

    file_name_part: str = "item"


class MinecraftObjectFactory:
    """Sets up all object factories at once."""

    _mods: "list[ModInfo]"
    block: BlockFactory
    enchantment: EnchantmentFactory
    entity: EntityFactory
    item: ItemFactory

    @property
    def mods(self) -> "list[ModInfo]":
        return self._mods

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self._mods = mods
        self.block = BlockFactory(mods)
        self.enchantment = EnchantmentFactory(mods)
        self.entity = EntityFactory(mods)
        self.item = ItemFactory(mods)

    def import_mod(self, mod: ModInfo) -> None:
        """Imports configs from file for all factories.

        Args:
            mod (ModInfo): describes object collection to be imported
        """
        self.block.import_mod(mod)
        self.enchantment.import_mod(mod)
        self.entity.import_mod(mod)
        self.item.import_mod(mod)
