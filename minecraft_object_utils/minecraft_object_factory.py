from .base_factory import BaseObjectFactory
from .block import Block, BlockTraits
from .enchantment import Enchantment, EnchantmentTraits
from .entity import Entity, EntityTraits
from .item import ItemStack, ItemTraits
from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class BlockFactory(BaseObjectFactory[Block, BlockTraits]):
    """Registers BlockTraits and allows creation of Block instances from them."""

    file_name_part: str = "block"
    BaseObjType: type = Block
    BaseObjTraitType: type = BlockTraits


class EnchantmentFactory(BaseObjectFactory[Enchantment, EnchantmentTraits]):
    """Registers EnchantmentTraits and allows creation of Enchantment instances from them."""

    file_name_part: str = "enchantment"
    BaseObjType: type = Enchantment
    BaseObjTraitType: type = EnchantmentTraits


class EntityFactory(BaseObjectFactory[Entity, EntityTraits]):
    """Registers EntityTraits and allows creation of Entity instances from them."""

    file_name_part: str = "entity"
    BaseObjType: type = Entity
    BaseObjTraitType: type = EntityTraits


class ItemFactory(BaseObjectFactory[ItemStack, ItemTraits]):
    """Registers ItemTraits and allows creation of ItemStack instances from them."""

    file_name_part: str = "item"
    BaseObjType: type = ItemStack
    BaseObjTraitType: type = ItemTraits


class MinecraftObjectFactory:
    """Sets up Block, Item, and Entity factories."""

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
