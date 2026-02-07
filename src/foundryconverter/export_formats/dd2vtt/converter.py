from foundryconverter.import_formats.foundry.types import FoundryWithLevelsFormat
from foundryconverter.export_formats.dd2vtt.types import DungeonDraftLevel
from foundryconverter.export_formats.types import (
    BaseConverterClass,
    BaseConverterConfig,
)

from pydantic import BaseModel, Field
from typing import Any


class ExtraConfig(BaseModel):
    lightanimation: str | None = None
    # TODO add more here


class ConfigData(BaseConverterConfig):
    extra_config: ExtraConfig | None = None
    final_file_format: str = Field(default="json")


class ConvertDD2ToFoundry(BaseConverterClass):
    import_class = DungeonDraftLevel
    export_class = FoundryWithLevelsFormat
    config_class = ConfigData
    object_data: list[DungeonDraftLevel]

    def __init__(self, config_object: ConfigData | Any):
        for floor in config_object.floor_objects:
            self.object_data.append(
                self.convert_from_json(self.read_from_file(floor.json_location))
            )

    @staticmethod
    def configure_config_data(data) -> ConfigData:
        return ConfigData(**data)

    def setup_objects(self) -> FoundryWithLevelsFormat:
        data = FoundryWithLevelsFormat()
        return data
