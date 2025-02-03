import dataclasses
from enum import Enum


class OscilloscopeType(Enum):
    BASIC = 0
    BASIC_LIGHTING = 1
    BLUR_LIGHTING = 2


@dataclasses.dataclass
class OscilloscopeStyle:
    type: OscilloscopeType
    color: tuple[int, int, int, int]
    step: float = 1

    blur_range: float | None = None
    blur_focus_level: float | None = None