import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1'

from softscope.oscilloscope_renderer import OscilloscopeRenderer

from softscope import audio_player
from softscope import oscilloscope_style
from softscope import typing

from softscope import file_scope
from softscope import mic_scope
from softscope import check

__all__ = [
    'OscilloscopeRenderer',
    'audio_player',
    'oscilloscope_style',
    'typing',

    'file_scope',
    'mic_scope',
    'check'
]