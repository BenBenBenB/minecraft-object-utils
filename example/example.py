from minecraft_object_utils import (
    BlockProperty,
    BlockTraits,
    MinecraftObjectFactory,
    ModInfo,
)

# Basic Example:
mcof = MinecraftObjectFactory()
block1 = mcof.block.create("dirt")  # same result as "minecraft:dirt"
item1 = mcof.item.create("minecraft:egg")  # same result as "egg"
entity1 = mcof.entity.create("chicken")

# Example: create a dispenser and set a block state.
block2 = mcof.block.create("dispenser")
print(block2.get_state("facing"))  # default is "north"  # noqa: T201
block2.set_state("facing", "east")
print(block2.get_state("facing"))  # noqa: T201
try:
    block2.set_state("triggered", "very")  # will error, invalid state
except ValueError as error:
    print(error)  # noqa: T201
try:
    block2.set_state("color", "red")  # will error, invalid property
except ValueError as error:
    print(error)  # noqa: T201

# You can also specify initial block state values with keyword arguments
block3 = mcof.block.create("repeater", facing="south", delay=4)


# Example: for Create mod v0.5.0i, make "/your/configs/dir/create-0.5.0i-block.toml" and import:
mods = [
    ModInfo("minecraft", "1.19"),
    ModInfo("create", "0.5.0i", "/your/configs/dir"),
]
mcof_mods = MinecraftObjectFactory(mods)

# You can also register info to a factory manually.
cust_f = MinecraftObjectFactory([])
bt1 = BlockTraits("yourmod:yourblock")  # block with no state
bt2 = BlockTraits(
    "othermod:otherblock",
    props=[
        BlockProperty("awesome", False, [True, False]),
        BlockProperty("fakename", "foo", ["foo", "bar", "baz"]),
    ],
)

cust_f.block.register(bt1)
cust_f.block.register(bt2)
block5 = cust_f.block.create("yourmod:yourblock")
block6 = cust_f.block.create("othermod:otherblock")
block6.set_state("awesome", True)
