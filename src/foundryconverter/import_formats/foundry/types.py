from pydantic import BaseModel, Field, ValidationError, BeforeValidator
import random
import string
from enum import Enum
from typing import Annotated


def ensure_coord_length(value: list):
    if len(value) != 4:
        raise ValidationError
    return value


class WallAnimationChoices(Enum):
    swing = "swing"


class WallAnimationObject(BaseModel):
    type: WallAnimationChoices
    texture: str
    flip: bool
    double: bool
    direction: int
    duration: int
    strength: int


class WallThresholdObject(BaseModel):
    light: int | None = Field(default=None)
    sight: int | None = Field(default=None)
    sound: int | None = Field(default=None)
    attenuation: bool = Field(default=False)


class WallsObject(BaseModel):
    light: int = Field(default=20)
    sight: int = Field(default=20)
    sound: int = Field(default=20)
    move: int = Field(default=20)
    c: Annotated[list[int], BeforeValidator(ensure_coord_length)]
    dir: int = Field(default=0)
    door: int = Field(default=0)
    ds: int = Field(default=0)
    threshold: WallThresholdObject = Field(default=WallThresholdObject())
    flags: dict = Field(default=dict())
    levels: list[str | None] = Field(default=list())
    animation: WallAnimationObject | None = Field(default=None)


class DarknessObject(BaseModel):
    min: float = Field(default=0)
    max: float = Field(default=1)


class LightAnimationChoices(Enum):
    flame = "flame"


class LightAnimationObject(BaseModel):
    type: LightAnimationChoices
    speed: float = Field(default=1)
    intensity: float = Field(default=1)
    reverse: bool = Field(default=False)


class LightConfigObject(BaseModel):
    alpha: float
    angle: int = Field(default=360)
    bright: float
    color: str = Field(default="#FFAD00")
    coloration: float = Field(default=1)
    dim: float
    attenuation: float = Field(default=1)
    luminosity: float = Field(default=0.5)
    saturation: float = Field(default=0)
    contrast: float = Field(default=0)
    shadows: float = Field(default=0)
    animation: LightAnimationObject | None = Field(default=None)
    darkness: DarknessObject = Field(default=DarknessObject())
    negative: bool = Field(default=False)
    priority: float = Field(default=0)


class LightObject(BaseModel):
    x: int
    y: int
    rotation: float = Field(default=0)
    walls: bool = Field(default=True)
    vision: bool = Field(default=False)
    config: LightConfigObject
    hidden: bool = Field(default=False)
    flags: dict = Field(default=dict())
    elevation: int
    levels: list[str | None] = Field(default=list())
    name: str = Field(default="")
    locked: bool = Field(default=False)


class ElevationObject(BaseModel):
    bottom: int
    top: int


class LevelTextureObject(BaseModel):
    anchorX: float = Field(default=0.5)
    anchorY: float = Field(default=0.5)
    fit: str = Field(default="fill")
    offsetX: float = Field(default=0)
    offsetY: float = Field(default=0)
    rotation: float = Field(default=0)
    scaleX: float = Field(default=1)
    scaleY: float = Field(default=1)


class LevelImageobject(BaseModel):
    alphaThreshold: float = Field(default=0)
    # TODO: check to see if i can add the image in raw here
    src: str | None = Field(default=None)
    tint: str = Field(default="#ffffff")
    color: str = Field(default="#232f28")


class LevelsObject(BaseModel):
    id: str = Field(alias="_id")
    name: str
    background: LevelImageobject = Field(default=LevelImageobject())
    textures: LevelTextureObject = Field(default=LevelTextureObject())
    elevation: ElevationObject
    foreground: LevelImageobject = Field(default=LevelImageobject())
    fog: dict = Field(default={"src": None, "tint": "#ffffff"})
    visibility: dict[str, list[str] | None] = Field(default=dict())
    sort: float = Field(default=0)
    flags: dict = Field(default=dict())

    @staticmethod
    def id_generator(level=-1, size=16, chars=string.ascii_letters + string.digits):
        if level == 0:
            return "defaultLevel0000"
        return "".join(random.choice(chars) for _ in range(size))


class BasicStats(BaseModel):
    coreVersion: str = Field(default="14.354")
    systemIdstr: str = Field(default="dnd5e")
    systemVersionstr: str = Field(default="5.2.4")


class StatsObject(BasicStats):
    duplicateSource: None = Field(default=None)
    exportSource: BasicStats = Field(default=BasicStats())


class InitialPostitionObject(BaseModel):
    x: int = Field(default=0)
    y: int = Field(default=0)
    scale: float = Field(default=0)

    @staticmethod
    def calculate_initial_position() -> "InitialPostitionObject": ...


class LightingObject(BaseModel):
    hue: float = Field(default=0)
    intensity: float = Field(default=0)
    luminosity: float = Field(default=0)
    saturation: float = Field(default=0)
    shadows: float = Field(default=0)


class GlobalLightObject(BaseModel):
    enabled: bool = Field(default=True)
    alpha: float = Field(default=0.5)
    bright: bool = Field(default=False)
    color: str | None = Field(default=None)
    coloration: float = Field(default=1)
    luminosity: float = Field(default=0)
    saturation: float = Field(default=0)
    contrast: float = Field(default=0)
    shadows: float = Field(default=0)
    darkness: DarknessObject = Field(default=DarknessObject())


class EnvironmentObject(BaseModel):
    darknessLevel: float = Field(default=0)
    darknessLock: bool = Field(default=False)
    globalLight: GlobalLightObject = Field(default=GlobalLightObject())
    cycle: bool = Field(default=True)
    base: LightingObject = Field(default=LightingObject())
    dark: LightingObject = Field(
        default=LightingObject(**{"hue": 0.7138888888888889, "luminosity": -0.25})
    )


class FogColoursObject(BaseModel):
    explored: str | None = Field(default=None)
    unexplored: str | None = Field(default=None)


class FogObject(BaseModel):
    mode: int = Field(default=1)
    colors: FogColoursObject = Field(default=FogColoursObject())


class GridObject(BaseModel):
    type: int = Field(default=1)
    size: float
    style: str = Field(default="solidLines")
    thickness: float = Field(default=1)
    color: str = Field(default="#000000")
    alpha: float = Field(default=1)
    distance: float = Field(default=0.2)
    units: str = Field(default="ft")


class FoundryWithLevelsFormat(BaseModel):
    name: str
    navigation: bool = Field(default=False)
    width: int
    height: int
    padding: float
    grid: GridObject
    shiftX: float = Field(default=0)
    shiftY: float = Field(default=0)
    tokenVision: bool = Field(default=True)
    fog: FogObject = Field(default=FogObject())
    environment: EnvironmentObject
    initial: InitialPostitionObject | dict = Field(default=dict())
    transition: dict = Field(
        default={"type": "fade", "duration": 1500, "activeOnly": True}
    )
    drawings: list = Field(default=list())
    tokens: list = Field(default=list())
    levels: list[LevelImageobject] | list = Field(default=list())
    lights: list[LightingObject] | list = Field(default=list())
    notes: list = Field(default=list())
    sounds: list = Field(default=list())
    regions: list = Field(default=list())
    tiles: list = Field(default=list())
    walls: list[WallsObject] | list = Field(default=list())
    navOrder: float = Field(default=0)
    navName: str = Field(default="")
    stats: StatsObject = Field(default=StatsObject(), alias="_stats")
    initialLevel: str | None = Field(default=None)
