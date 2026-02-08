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
from foundryconverter.export_formats.dd2vtt.types import DungeonDraftLevel
from foundryconverter.export_formats.types import (
    BaseConverterClass,
    BaseConverterConfig,
)
import os
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
    object_data: list[DungeonDraftLevel]
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
        example_level = self.object_data[0]
        grid_scale = example_level.resolution.pixels_per_grid
        for i, (level, floor) in enumerate(
            zip(self.object_data, self.config_object.floor_objects)
        ):
            levels_object = LevelsObject(
                _id=LevelsObject.id_generator(i),
                name=os.path.basename(floor.json_location),
                elevation=ElevationObject(
                    bottom=floor.start_height, top=floor.end_height
                ),
            )
            levels.append(levels_object)
            for light in level.lights:
                light_colour = "#" + light.color[0:6]
                light_alpha = int(light.color[-2:], 16) / 255
                lights.append(
                    LightObject(
                        x=int(light.position.x * grid_scale),
                        y=int(light.position.y * grid_scale),
                        levels=[levels_object.id],
                        elevation=levels_object.elevation.bottom,
                        config=LightConfigObject(
                            dim=light.range,
                            bright=light.range,
                            color=light_colour,
                            alpha=light_alpha,
                        ),
                    )
                )
                for wall in level.line_of_sight:
                    split_list = []
                    for i in range(len(wall)):
                        if i == (len(wall) - 1):
                            break
                        split_list.append(
                            [
                                *wall[i].model_dump().values(),
                                *wall[i + 1].model_dump().values(),
                            ]
                        )
                    for updated_wall in split_list:
                        walls.append(
                            WallsObject(
                                levels=[levels_object.id],
                                c=[int(w * grid_scale) for w in updated_wall],
                                door=0,
                            )
                        )
                for door in level.portals:
                    updated_bounds = [
                        *door.bounds[0].model_dump().values(),
                        *door.bounds[1].model_dump().values(),
                    ]
                    walls.append(
                        WallsObject(
                            levels=[levels_object.id],
                            c=[int(b * grid_scale) for b in updated_bounds],
                            door=1,
                        )
                    )

        example_level = self.object_data[0]
        if example_level.environment.ambient_light:
            global_colour = "#" + example_level.environment.ambient_light[0:6]
            global_alpha = int(example_level.environment.ambient_light[-2:], 16) / 255
        else:
            global_colour = None
            global_alpha = 0
        data = FoundryWithLevelsFormat(
            name=self.config_object.map_name,
            grid=GridObject(size=grid_scale),
            width=int(grid_scale * example_level.resolution.map_size.x),
            height=int(grid_scale * example_level.resolution.map_size.y),
            padding=0,
            walls=walls,
            lights=lights,
            levels=levels,
            environment=EnvironmentObject(
                globalLight=GlobalLightObject(
                    enabled=example_level.environment.baked_lighting,
                    color=global_colour,
                    alpha=global_alpha,
                ),
            ),
            initialLevel=levels[self.config_object.initial_level].id,
        )
        return data
