import dataclasses
from enum import Enum


class OscilloscopeType(Enum):
    # 지정된 순수 컬러로만 선을 그림
    BASIC = 0

    # 지정된 컬러 기반으로 그리되, 선이 지나가는 속도를 계산하여 밝기를 일부 조정함
    BASIC_LIGHTING = 1

    # 선이 지나가는 속도를 계산하여 밝기를 일부 조절하고 그려진 결과에 합성곱을 통한 블러를 입힘
    BLUR_LIGHTING = 2


@dataclasses.dataclass
class OscilloscopeStyle:
    """
    오실로스코프의 렌더링 스타일을 설정하는 객체.
    오실로스코프의 빛 계산이나, 색상과 관련된 부분을 맡으며
    보이는 크기나 그래프 증폭률처럼 모양과 관련된 옵션은 포함하지 않음
    """
    type: OscilloscopeType
    color: tuple[int, int, int, int]

    blur_range: float | None = None
    blur_focus_level: float | None = None