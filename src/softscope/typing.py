import numpy
from numpy.typing import NDArray

AudioData = NDArray[NDArray[numpy.float64]]
# [
#   [float64, float64],
#   [float64, float64],
#   [float64, float64], ...
# ]
SingleSample = NDArray[numpy.float64]
# [float64, float64]