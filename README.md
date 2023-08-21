# Minecraft Object Utils

> A python library for creating objects that represent blocks, items, and entities from Minecraft Java Edition.

**Features**
- Support for multiple versions of vanilla Minecraft
- Support for modded Minecraft by importing from custom toml files
- Ensure that block states are valid

## Basic Usage

### Vanilla Minecraft
The default constructor will reflect objects from the latest version of minecraft. The minecraft namespace is assumed if one is not supplied in the block name.

Basic Example: create a dirt block.
```python
from minecraft_object_utils import *
mcof = MinecraftObjectFactory()
block1 = mcof.blocks.create("dirt") # same result as "minecraft:dirt"
```

Example: create a dispenser, which has powered and facing states.
```python
mcof = MinecraftObjectFactory()
block2 = mcof.blocks.create("dispenser")
block2.get_state('facing')  # default is "north"
block2.set_state('powered', True)
block2.set_state('powered', "very")  # will error, invalid state
block2.set_state('color', "red")  # will error, invalid property
```

### Modded Minecraft
You can create and import toml files to represent objects from mods.

Example: for Create mod v0.5.0i, make "/your/configs/dir/create-0.5.0i-blocks.toml" and import:
```python
mods = [ 
    ModInfo("minecraft","1.19.2"), 
    ModInfo("create","0.5.0i", "/your/configs/dir") 
]
mcof = MinecraftObjectFactory(mods)
block3 = mcof.blocks.create("stone") # assumes "minecraft:stone"
block4 = mcof.blocks.create("create:chute")
```

You can also register block info to the factory manually. 
Example:
```python
bf = BlockFactory([])
bt1 = BlockTraits("yourmod:yourblock")  # block with no state
bt2 = BlockTraits(
    "othermod:otherblock",
    [
        BlockProperty('awesome', False, [True, False]),
        BlockProperty('fakename', "foo", ["foo", "bar", "baz"]),
    ],
)

bf.register(bt1)
bf.register(bt2)
block1 = bf.create("yourmod:yourblock")
block2 = bf.create("othermod:otherblock")
block2.set_state('awesome', True)
```

### Generating toml files

I generated the blocks file by running Minecraft out of IntelliJ. I'd like to make a fabric/forge mod that can output these files. For now, here is the relevant code for obtaining block states from Minecraft itself:
```java
Minecraft minecraft = Minecraft.getInstance();
ClientLevel level = minecraft.level;
Registry<Block> blocks = level.registryAccess().registry(Registries.BLOCK).get();

String newLine = "\r\n";
String filePath = "C:\\src\\output\\block_data.toml";
File newFile = new File(filePath);

try {
    FileWriter myWriter = new FileWriter(filePath);
    myWriter.write(format("# Generated from Minecraft version %s", minecraft.getLaunchedVersion()));
    myWriter.write(newLine);

    for (var block : blocks) {
        final String blockId = blocks.getKey(block).getPath().toLowerCase();
        final var statesProps = block.getStateDefinition().getProperties();

        // [{block_id}]
        myWriter.write(format("[%s]", blockId));
        myWriter.write(newLine);
        for (var prop : statesProps){
            // [{block_id}.properties.{prop_name}]
            final String propName = prop.getName().toLowerCase();
            myWriter.write(format("[%s.properties.%s]", blockId, propName));
            myWriter.write(newLine);

            // default = {default}
            final var defaultValue = block.defaultBlockState().getValue(prop);
            myWriter.write(format("default = \"%s\"", defaultValue.toString().toLowerCase()));
            myWriter.write(newLine);

            // allowed = [{val_1, val_2 ..., val_n}]
            final var allowed = prop.getPossibleValues()
                    .stream()
                    .map(String::valueOf)
                    .collect(Collectors.joining("\", \""));
            myWriter.write(format("allowed = [\"%s\"]", allowed.toLowerCase()));
            myWriter.write(newLine);
        }
    }
    myWriter.close();
    System.out.println("Successfully wrote to the file.");
} catch (IOException e) {
    System.out.println("An error occurred.");
}
```

