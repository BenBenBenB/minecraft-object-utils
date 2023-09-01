from minecraft_object_utils import MinecraftObjectFactory

mcof = MinecraftObjectFactory()
# create inventory block
chest = mcof.block.create("chest")

# add items to inventory slots
chest.inventory[0] = mcof.item.create(
    "wooden_sword",
    enchantments=[
        mcof.enchantment.create("mending"),
        mcof.enchantment.create("unbreaking", level=3),
        mcof.enchantment.create("sharpness", level=5),
    ],
)
chest.inventory[26] = mcof.item.create(
    "enchanted_golden_apple",
    count=64,
)
