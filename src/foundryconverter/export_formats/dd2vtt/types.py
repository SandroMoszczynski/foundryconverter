from pydantic import BaseModel, Field


class PositionOjbect(BaseModel):
    x: float
    y: float


class ResolutionObject(BaseModel):
    map_origin: PositionOjbect
    map_size: PositionOjbect
    pixels_per_grid: int


class PortalObject(BaseModel):
    position: PositionOjbect
    bounds: list[PositionOjbect]
    rotation: int
    closed: bool
    freestanding: bool


class EnvironmentObject(BaseModel):
    baked_light: bool
    ambient_light: str


class LightObject(BaseModel):
    position: PositionOjbect
    range: int
    intensity: int
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
