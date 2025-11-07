# Copyright 2025 QuantInsti Quantitative Learnings Pvt Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import numpy
from typing import Any, cast
from blueshift.lib.common.sentinels import NotSpecified, Sentinel

from ..data import BoundColumn
from .factors import Factor, CustomFactor
from ..filters import Filter
from blueshift.types import Asset

class RollingPearson(CustomFactor):
    """ rolling pearson correlation. """
    def __init__(self, base_factor:Factor|BoundColumn, target:Factor|BoundColumn, 
                 correlation_length:int, mask:Filter|Sentinel=NotSpecified) -> None: ...
    ...

class RollingSpearman(CustomFactor):
    """ rolling spearman correlation. """
    def __init__(self, base_factor:Factor|BoundColumn, target:Factor|BoundColumn, 
                 correlation_length:int, mask:Filter|Sentinel=NotSpecified) -> None: ...
    ...

class RollingLinearRegression(CustomFactor):
    """ rolling regression. """
    def __init__(self, dependent:Factor, independent:Factor, regression_length:int, 
                 mask:Filter|Sentinel=NotSpecified) -> None: ...
    ...

class RollingPearsonOfReturns(RollingPearson):
    """ rolling pearson correlation of returns. """
    def __init__(self, target: Asset, returns_length: int, correlation_length: int, 
                 mask: Filter | Sentinel = NotSpecified) -> None: ...
    ...

class RollingSpearmanOfReturns(RollingSpearman):
    """ rolling spearmna correlation of returns. """
    def __init__(self, target: Asset, returns_length: int, correlation_length: int, 
                 mask: Filter | Sentinel = NotSpecified) -> None: ...
    ...

class RollingLinearRegressionOfReturns(RollingLinearRegression):
    """ rolling regression of returns of all assets against `target`. """
    def __init__(self, target: Asset, returns_length: int, regression_length: int, 
                 mask: Filter | Sentinel = NotSpecified) -> None: ...
    ...

class SimpleBeta(CustomFactor):
    """ simple beta of assets against the `target`. """
    def __init__(self, target: Asset, regression_length: int, 
                 allowed_missing_percentage:float=0.25) -> None: ...
    ...

def vectorized_beta(dependents:numpy.ndarray, independent:numpy.ndarray, allowed_missing:int, 
                    out:numpy.ndarray|None=None) -> numpy.ndarray:
    """ compute slopes of linear regressions between `dependents` and `independent`."""
    ...

def vectorized_pearson_r(dependents:numpy.ndarray, independent:numpy.ndarray, allowed_missing:int, 
                    out:numpy.ndarray|None=None) -> numpy.ndarray:
    """ compute pearson correlation between `dependents` and `independent`."""
    ...