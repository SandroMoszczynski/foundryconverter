from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated


def discard_negative(value: float | int):
    if value < 0:
        return 0
    return value


class PositionOjbect(BaseModel):
    x: Annotated[float | int, BeforeValidator(discard_negative)]
    y: Annotated[float | int, BeforeValidator(discard_negative)]


class ResolutionObject(BaseModel):
    map_origin: PositionOjbect
    map_size: PositionOjbect
    pixels_per_grid: int


class PortalObject(BaseModel):
    position: PositionOjbect
    bounds: list[PositionOjbect]
    rotation: float
    closed: bool
    freestanding: bool


class EnvironmentObject(BaseModel):
    baked_lighting: bool
    ambient_light: str


class LightObject(BaseModel):
    position: PositionOjbect
    range: float
    intensity: float
    color: str
    shadows: bool = Field(default=True)


class DungeonDraftLevel(BaseModel):
    format: float
    resolution: ResolutionObject
    line_of_sight: list[list[PositionOjbect]]
    objects_line_of_sight: list = Field(default=list(()))
    portals: list[PortalObject]
    environment: EnvironmentObject
    lights: list[LightObject]
    image: str
