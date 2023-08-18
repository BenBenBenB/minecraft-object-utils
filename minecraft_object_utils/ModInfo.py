import os.path

VANILLA_NAMESPACE = "minecraft"
DEFAULT_DATA_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")

class ModInfo:
    namespace: str
    version: str
    directory: str

    @property
    def versioned_name(self) -> str:
        return f"{self.namespace}-{self.version}"

    def __init__(
        self, namespace: str, version: str = "", directory: str = ""
    ) -> None:
        self.namespace = namespace
        self.version = version
        if directory == "":
            self.directory = DEFAULT_DATA_DIRECTORY
        else:
            self.directory = directory


VANILLA_JAVA_LATEST = ModInfo(VANILLA_NAMESPACE, "1.20")
