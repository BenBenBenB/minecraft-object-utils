from BlockFactory import BlockFactory
from ModInfo import VANILLA_JAVA_LATEST, ModInfo


class MinecraftObjectFactory:
    _mods: "list[ModInfo]"
    blocks: BlockFactory
    # items: ItemFactory
    # entities: EntityFactory

    @property
    def mods(self) -> "list[ModInfo]":
        return self._mods

    def __init__(self, mods: "list[ModInfo]" = [VANILLA_JAVA_LATEST]) -> None:
        self._mods = mods
        self.blocks = BlockFactory(mods)
        # self.items = ItemFactory(mods)
        # self.entities = EntityFactory(mods)

    def import_namespace(self, mod: ModInfo) -> None:
        imported_already = [n for n in self._mods if n.namespace == mod.namespace]
        if any(imported_already):
            imported_name = (
                f"{imported_already[0].namespace}-{imported_already[0].version}"
            )
            raise ValueError(
                f"Skipping import for {mod.namespace}. Already imported for same name: {imported_name}"
            )
        self.blocks.import_namespace(mod)
        # self.items.import_namespace(mod)
        # self.entities.import_namespace(mod)
