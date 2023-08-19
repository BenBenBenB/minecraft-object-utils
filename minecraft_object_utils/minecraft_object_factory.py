from .block_factory import BlockFactory
from .entity_factory import EntityFactory
from .item_factory import ItemFactory
from .mod_info import VANILLA_JAVA_LATEST, ModInfo


class MinecraftObjectFactory:
    """Sets up Block, Item, and Entity factories."""

    _mods: "list[ModInfo]"
    blocks: BlockFactory
    items: ItemFactory
    entities: EntityFactory

    @property
    def mods(self) -> "list[ModInfo]":
        return self._mods

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self._mods = mods
        self.blocks = BlockFactory(mods)
        self.items = ItemFactory(mods)
        self.entities = EntityFactory(mods)

    def import_namespace(self, mod: ModInfo) -> None:
        """Imports configs from file for all factories.

        Args:
            mod (ModInfo): namespaces to be imported
        """
        imported_already = [n for n in self._mods if n.namespace == mod.namespace]
        if any(imported_already):
            raise ValueError(
                f"Problem importing {mod.versioned_name}. Conflict with {imported_already[0].versioned_name}"
            )
        self.blocks.import_namespace(mod)
        self.items.import_namespace(mod)
        self.entities.import_namespace(mod)
