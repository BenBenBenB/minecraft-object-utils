import os.path

VANILLA_NAMESPACE = "minecraft"
DEFAULT_DATA_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")

class ModInfo:
    namespace: str
    version: str
    directory: str

    def __init__(
        self, namespace: str, version: str = "", directory: str = ""
    ) -> None:
        self.namespace = namespace
        self.version = version
        if directory == "":
            self.directory = os.path.join(DEFAULT_DATA_DIRECTORY, namespace)
        else:
            self.directory = directory


VANILLA_JAVA_LATEST = ModInfo(VANILLA_NAMESPACE, "1.20")
