import os.path

VANILLA_NAMESPACE = "minecraft"
VANILLA_DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), "data")


class ModInfo:
    namespace: str
    version: str
    directory: str

    @property
    def versioned_name(self) -> str:
        return f"{self.namespace}-{self.version}"

    def __init__(
        self, namespace: str, version: str, directory: str = VANILLA_DATA_DIRECTORY
    ) -> None:
        self.namespace = namespace
        self.version = version
        self.directory = directory

    def get_file_path(self, factory_name: str) -> str:
        return os.path.join(
            self.directory, f"{self.versioned_name}-{factory_name}.toml"
        )


VANILLA_JAVA_LATEST = ModInfo(VANILLA_NAMESPACE, "1.20", VANILLA_DATA_DIRECTORY)
