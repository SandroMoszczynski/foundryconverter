from foundryconverter.import_formats.foundry.types import (
    FoundryWithLevelsFormat,
    LevelsObject,
    ElevationObject,
    LightObject,
    WallsObject,
    LightConfigObject,
    GridObject,
    EnvironmentObject,
    GlobalLightObject,
)
from foundryconverter.export_formats.dungeon_alchemist.types import (
    DungeonAlchemistLevel,
)
from pydantic import BaseModel, Field
from foundryconverter.export_formats.types import (
    BaseConverterClass,
    BaseConverterConfig,
)
from typing import Any


class ExtraConfig(BaseModel):
    lightanimation: str | None = None
    # TODO add more here


class ConfigData(BaseConverterConfig):
    extra_config: ExtraConfig | None = None
    final_file_format: str = Field(default="json")


class ConvertDAToFoundry(BaseConverterClass):
    import_class = DungeonAlchemistLevel
    export_class = FoundryWithLevelsFormat
    object_data: list[DungeonAlchemistLevel]
    config_class = ConfigData

    def __init__(self, config_object: ConfigData | Any):
        self.config_object = config_object
        self.object_data = []
        for floor in config_object.floor_objects:
            self.object_data.append(
                self.convert_from_json(self.read_from_file(floor.json_location))
            )

    def setup_objects(self) -> FoundryWithLevelsFormat:
        levels: list[LevelsObject] = []
        lights: list[LightObject] = []
        walls: list[WallsObject] = []
        for i, (level, floor) in enumerate(
            zip(self.object_data, self.config_object.floor_objects)
        ):
            levels_object = LevelsObject(
                _id=LevelsObject.id_generator(i),
                name=level.name,
                elevation=ElevationObject(
                    bottom=floor.start_height, top=floor.end_height
                ),
            )
            levels.append(levels_object)
            for light in level.lights:
                lights.append(
                    LightObject(
                        x=light.x,
                        y=light.y,
                        levels=[levels_object.id],
                        elevation=levels_object.elevation.bottom,
                        config=LightConfigObject(
                            dim=light.dim,
                            bright=light.bright,
                            color=light.tintColor,
                            alpha=light.tintAlpha,
                        ),
                    )
                )
            for wall in level.walls:
                walls.append(
                    WallsObject(
                        levels=[levels_object.id],
                        c=wall.c,
                        door=wall.door,
                    )
                )

        # TODO, perhaps pass in the required parts in the config data?
        example_level = self.object_data[0]

        data = FoundryWithLevelsFormat(
            name=self.config_object.map_name,
            grid=GridObject(
                size=example_level.grid,
                units=example_level.gridUnits,
                distance=example_level.gridDistance,
                color=example_level.gridColor,
                alpha=example_level.gridAlpha,
            ),
            width=example_level.width,
            height=example_level.height,
            padding=example_level.padding,
            walls=walls,
            lights=lights,
            levels=levels,
            environment=EnvironmentObject(
                darknessLevel=example_level.darkness,
                globalLight=GlobalLightObject(enabled=example_level.globalLight),
            ),
            initialLevel=levels[self.config_object.initial_level].id,
        )
        return data
