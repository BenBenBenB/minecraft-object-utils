# Minecraft Object Utils

> A python library for creating objects that represent blocks, items, and entities from Minecraft Java Edition.

**Features**
- Support for multiple versions of vanilla Minecraft
- Support for modded Minecraft by importing from custom toml files
- Ensure that block states are valid

## Basic Usage

### Vanilla Minecraft
The default constructor will reflect objects from the latest version of minecraft.
Basic Example: create a dirt block.
```python
from minecraft_object_utils import *
mcof = MinecraftObjectFactory()
block1 = mcof.blocks.create("dirt")
```

Create a dispenser, which has powered and facing states.
```python
mcof = MinecraftObjectFactory()
block2 = mcof.blocks.create("dispenser")
block2.facing # default is "north"
block2.powered = "true"
block2.powered = "very" # will error, invalid state value
block2.color = "red" # will error, invalid state name
```

### Modded Minecraft
You can restrict the available objects by minecraft version and/or mod:
If you created "0.5.0i-blocks.toml" for Create mod v0.5.0i:
```python
mods = [ 
    ModInfo("minecraft","1.19.2"), 
    ModInfo("create","0.5.0i", "/path/to/configs/dir") 
]
mcof = MinecraftObjectFactory(mods)
block3 = mcof.blocks.create("stone") # assumes "minecraft:stone"
block4 = mcof.blocks.create("create:chute")
```

You can also manage the dictionaries manually. Example:
```python
bf = BlockFactory()
bf.block_states["yourmod:yourblock"] = [] # block with no states.
bf.block_states["othermod:otherblock"] = [
    BlockState("awesome","false",["true","false"]),
    BlockState("fakestatename","foo",["foo","bar","baz"]),
]
block1 = bf.create("yourmod:yourblock")
block2 = bf.create("othermod:otherblock")
block2.awesome = "true"
```
