# Copyright 2024 QuantInsti Quantitative Learnings Pvt Ltd.
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
from typing import Callable, overload
import numpy
import pandas

from blueshift.lib.common.sentinels import NotSpecified, Sentinel

from ..term import ComputableTerm
from ..data import BoundColumn
from ..factors import Factor
from ..classifiers import Classifier

class Filter(ComputableTerm):
    """ A pipeline filter expression. """
    def __and__(self, other:Filter) -> Filter:
        ...

    def __or__(self, other:Filter) -> Filter:
        ...

    def __xor__(self, other:Filter) -> Filter:
        ...

    def __rand__(self, other:Filter) -> Filter:
        ...

    def __ror__(self, other:Filter) -> Filter:
        ...

    def __rxor__(self, other:Filter) -> Filter:
        ...

    def if_else(self, if_true:ComputableTerm, if_false:ComputableTerm) -> ComputableTerm:
        """ Create a term that selects values from one of two choices. """
        ...
    ...

class NumExprFilter(Filter):
    @classmethod
    def create(cls, expr, binds) -> NumExprFilter:
        """ create a filter based on numexpr"""
        ...
    ...

class NullFilter(Filter):
    """ filter indicating whether input values are missing from an input"""
    def __init__(self, term:ComputableTerm) -> None: ...
    ...

class NotNullFilter(Filter):
    """ filter indicating whether input values are **not** missing from an input"""
    def __init__(self, term:ComputableTerm) -> None: ...
    ...

class PercentileFilter(Filter):
    """filter representing assets falling between percentile bounds of a Factor."""
    def __init__(self, factor:ComputableTerm, min_percentile:float, max_percentile:float) -> None: ...
    ...

class CustomFilter(Filter):
    """ user-defined filter. """
    inputs:list[BoundColumn]
    window_length:int

    def compute(self, today:pandas.Timestamp, assets:list[int], out:numpy.ndarray, *inputs)->None:
        """ implement custom filter that updates the `out` array with boolean. """
        ...

class ArrayPredicate(Filter):
    """ apply a function `op` (with additional **args if required) to a pipeline term. """
    def __init__(self, term:ComputableTerm, op:Callable[[numpy.ndarray], numpy.ndarray], opargs) -> None: ...

class Latest(CustomFilter):
    """ get the latest value. """
    def __init__(self, inputs:list[BoundColumn|Factor], window_length:int|Sentinel=NotSpecified) -> None: ...
    ...

class MaximumFilter(Filter):
    """ select top asset. """
    def __init__(self, factor:Factor, groupby:Classifier|Sentinel=NotSpecified, 
                 mask:Filter|Sentinel=NotSpecified) -> None: ...

class All(CustomFilter):
    """ requires True for `window_length` consecutive observation. """
    def __init__(self, inputs:list[Filter], window_length:int) -> None: ...
    ...

class Any(CustomFilter):
    """ requires True for at least one of `window_length` consecutive observation. """
    def __init__(self, inputs:list[Filter], window_length:int) -> None: ...
    ...

class AtLeastN(CustomFilter):
    """ requires True for at least N of `window_length` consecutive observation. """
    def __init__(self, inputs:list[Filter], window_length:int, N:int) -> None: ...
    ...

__all__ = [
    'All',
    'Any',
    'ArrayPredicate',
    'AtLeastN',
    'CustomFilter',
    'Filter',
    'Latest',
    'MaximumFilter',
    'NotNullFilter',
    'NullFilter',
    'NumExprFilter',
    'PercentileFilter',
]
