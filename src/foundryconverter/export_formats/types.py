from abc import ABC, abstractmethod
import json
from typing import Any
from pydantic import BaseModel


class FloorObject(BaseModel):
    json_location: str
    start_height: int
    end_height: int


class BaseConverterConfig(BaseModel):
    file_name: str
    final_location: str
    final_file_format: str
    floors: int
    initial_level: int
    map_name: str
    wall_height: int  # for now
    floor_objects: list[FloorObject]

    def return_final_name(self):
        return f"{self.final_location}{self.file_name}.{self.final_file_format}"


class SetupVariables(BaseModel):
    input_format: str
    export_format: str
    final_location: str
    folder_location: str | None = None
    config_dict: BaseConverterConfig


class BaseConverterClass(ABC):
    import_class: Any
    export_class: Any
    config_class: Any

    @abstractmethod
    def __init__(self, config_data: Any): ...

    def read_from_file(self, file_location: str) -> dict:
        with open(file_location) as json_data:
            return json.load(json_data)

    def convert_from_json(self, raw_data: dict):
        return self.import_class(**raw_data)

    @abstractmethod
    def setup_objects(self):
        return self.export_class

    def save_to_file(self, data: BaseModel | Any, file_name: str):
        with open(file_name, "w") as final_write:
            json.dump(data.model_dump(by_alias=True), final_write)
