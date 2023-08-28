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
from minecraft_object_utils import MinecraftObjectFactory
mcof = MinecraftObjectFactory()
block1 = mcof.block.create("dirt")  # same result as "minecraft:dirt"
item1 = mcof.item.create("minecraft:egg")  # same result as "egg"
entity1 = mcof.entity.create("chicken")
```

Example: create blocks and set some properties.
```python
block2 = mcof.block.create("dispenser")
print(block2.get_state("facing"))  # default is "north"
block2.set_state("facing", "east")
print(block2.get_state("facing")) 
block2.set_state("triggered", "very")  # will error, invalid state
block2.set_state("color", "red")  # will error, invalid property

# You can also specify initial block state values with keyword arguments
block3 = mcof.block.create("repeater", facing="south", delay=4)
```

### Modded Minecraft
You can create and import toml files to represent objects from mods.

Example: for Create mod v0.5.0i, make "/your/configs/dir/create-0.5.0i-block.toml" and import:
```python
from minecraft_object_utils import MinecraftObjectFactory, ModInfo
mods = [
    ModInfo("minecraft", "1.19"),
    ModInfo("create", "0.5.0i", "/your/configs/dir"),
]
mcof_mods = MinecraftObjectFactory(mods)
block3 = mcof_mods.block.create("stone")  # assumes "minecraft:stone"
block4 = mcof_mods.block.create("create:chute")
```

You can also register info to a factory manually. 
Example:
```python
from minecraft_object_utils import BlockProperty, BlockTraits, MinecraftObjectFactory
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

