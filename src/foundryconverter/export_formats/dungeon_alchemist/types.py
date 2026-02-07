from pydantic import BaseModel, BeforeValidator, ValidationError
from typing import Annotated


def ensure_coord_length(value: list):
    if len(value) != 4:
        raise ValidationError
    return value


class WallsObject(BaseModel):
    c: Annotated[list[int], BeforeValidator(ensure_coord_length)]
    move: int
    sense: int
    sound: int
    door: int


class LightObject(BaseModel):
    x: int
    y: int
    dim: float
    bright: float
    tintColor: str
    tintAlpha: float


class DungeonAlchemistLevel(BaseModel):
    name: str
    width: int
    height: int
    grid: int
    shiftX: int
    shiftY: int
    gridDistance: float
    gridUnits: str
    padding: float
    gridColor: str
    gridAlpha: float
    globalLight: bool
    darkness: float
    lights: list[LightObject]
    walls: list[WallsObject]
    img: str | None
    foreground: str | None
