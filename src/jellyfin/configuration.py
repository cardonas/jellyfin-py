import json
from pathlib import Path

from Models.ConfigurationData import ConfigurationData


class Configuration:
    def __init__(self, *, file_path: Path | str):
        self.file_path = file_path
        ...

    def load_configuration(self) -> ConfigurationData:
        with open(self.file_path, "r") as f:
            data = json.load(f)
            api_key = data.get("apiKey")
            return ConfigurationData(api_key=api_key)
