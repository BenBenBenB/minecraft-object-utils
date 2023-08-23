from .block_factory import BlockFactory
from .entity_factory import EntityFactory
from .item_factory import ItemFactory
from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class MinecraftObjectFactory:
    """Sets up Block, Item, and Entity factories."""

    _mods: "list[ModInfo]"
    block: BlockFactory
    item: ItemFactory
    entity: EntityFactory

    @property
    def mods(self) -> "list[ModInfo]":
        return self._mods

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self._mods = mods
        self.block = BlockFactory(mods)
        self.item = ItemFactory(mods)
        self.entity = EntityFactory(mods)

    def import_mod(self, mod: ModInfo) -> None:
        """Imports configs from file for all factories.

        Args:
            mod (ModInfo): describes object collection to be imported
        """
        self.block.import_mod(mod)
        self.item.import_mod(mod)
        self.entity.import_mod(mod)
