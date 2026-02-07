from abc import ABC, abstractmethod
import json
from typing import Any
from pydantic import BaseModel


class BaseConverterConfig(BaseModel):
    file_name: str
    final_location: str
    final_file_format: str

    def return_final_name(self):
        return f"{self.final_location}{self.file_name}.{self.final_file_format}"


class BaseConverterClass(ABC):
    import_class: Any
    export_class: Any
    config_class: Any

    @abstractmethod
    def __init__(self, config_data: Any): ...

    @staticmethod
    @abstractmethod
    def configure_config_data(data) -> BaseConverterConfig: ...

    def read_from_file(self, file_location: str) -> dict:
        with open(file_location) as json_data:
            return json.load(json_data)

    def convert_from_json(self, raw_data: dict):
        return self.import_class(**raw_data)

    @abstractmethod
    def setup_objects(self):
        return self.export_class

    def save_to_file(self, data: BaseModel | Any, file_name: str):
        with open(f"{file_name}.json", "w") as final_write:
            json.dump(data.model_dump_json(), final_write)
