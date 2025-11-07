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
from typing import Literal, overload
import pandas
import numpy

from blueshift.lib.common.sentinels import NotSpecified, Sentinel

from ..term import ComputableTerm
from ..filters import Filter
from ..classifiers import Classifier
from ..data import BoundColumn

class Factor(ComputableTerm):
    """ a pipeline factor. """
    @overload
    def __add__(self, other:float|int) -> Factor:...

    @overload
    def __add__(self, other:Factor) -> Factor:...

    def __radd__(self, other:float|int) -> Factor:...

    @overload
    def __sub__(self, other:float|int) -> Factor:...

    @overload
    def __sub__(self, other:Factor) -> Factor:...

    def __rsub__(self, other:float|int) -> Factor:...

    @overload
    def __mul__(self, other:float|int) -> Factor:...

    @overload
    def __mul__(self, other:Factor) -> Factor:...

    def __rmul__(self, other:float|int) -> Factor:...

    @overload
    def __div__(self, other:float|int) -> Factor:...

    @overload
    def __div__(self, other:Factor) -> Factor:...

    def __rdiv__(self, other:float|int) -> Factor:...

    @overload
    def __truediv__(self, other:float|int) -> Factor:...

    @overload
    def __truediv__(self, other:Factor) -> Factor:...

    def __rtruediv__(self, other:float|int) -> Factor:...

    @overload
    def __mod__(self, other:float|int) -> Factor:...

    @overload
    def __mod__(self, other:Factor) -> Factor:...

    def __rmod__(self, other:float|int) -> Factor:...

    @overload
    def __pow__(self, other:float|int) -> Factor:...

    @overload
    def __pow__(self, other:Factor) -> Factor:...

    def __rpow__(self, other:float|int) -> Factor:...

    @overload
    def __lt__(self, other:float|int) -> Filter:...

    @overload
    def __lt__(self, other:Factor) -> Filter:...

    @overload
    def __gt__(self, other:float|int) -> Filter:...

    @overload
    def __gt__(self, other:Factor) -> Filter:...

    @overload
    def __le__(self, other:float|int) -> Filter:...

    @overload
    def __le__(self, other:Factor) -> Filter:...

    @overload
    def __ge__(self, other:float|int) -> Filter:...

    @overload
    def __ge__(self, other:Factor) -> Filter:...

    @overload
    def __ne__(self, other:float|int) -> Filter:...

    @overload
    def __ne__(self, other:Factor) -> Filter:... # type: ignore[override]

    @overload
    def __eq__(self, other:float|int) -> Filter:...

    @overload
    def __eq__(self, other:Factor) -> Filter:... # type: ignore[override]

    def demean(self, mask:Filter|Sentinel=NotSpecified, 
               groupby:Classifier|Sentinel=NotSpecified) -> Factor:
        """ demean a factor. """
        ...

    def zscored(self, mask:Filter|Sentinel=NotSpecified, 
               groupby:Classifier|Sentinel=NotSpecified) -> Factor:
        """ compute zscore from a factor. """
        ...

    def rank(self, method:Literal['ordinal', 'min', 'max', 'dense', 'average']='ordinal',
             ascending:bool=True,
             mask:Filter|Sentinel=NotSpecified,
             groupby:Classifier|Sentinel=NotSpecified) -> Factor:
        """ create ranks from a factor. """
        ...

    def pearsonr(self, target:ComputableTerm, correlation_length:int, 
                 mask:Filter|Sentinel=NotSpecified) -> Factor:
        """ compute rolling pearson correlation. """
        ...

    def spearmanr(self, target:ComputableTerm, correlation_length:int, 
                 mask:Filter|Sentinel=NotSpecified) -> Factor:
        """ compute rolling spearmanr correlation. """
        ...

    def linear_regression(self, target:ComputableTerm, regression_length:int, 
                 mask:Filter|Sentinel=NotSpecified) -> Factor:
        """ compute rolling linear regression. """
        ...

    def winsorize(self, min_percentile:float, max_percentile:float, 
                 mask:Filter|Sentinel=NotSpecified,
                 groupby:Classifier|Sentinel=NotSpecified) -> Factor:
        """ clip the factor tails within the min and max percentile. """
        ...

    def quantiles(self, bins:int, mask:Filter|Sentinel=NotSpecified) -> Factor:
        """ compute qualtiles from the factor. """
        ...

    def quartiles(self, mask:Filter|Sentinel=NotSpecified) -> Factor:
        """ compute quartile. """
        ...

    def quintiles(self, mask:Filter|Sentinel=NotSpecified) -> Factor:
        """ compute quintiles. """
        ...

    def deciles(self, mask:Filter|Sentinel=NotSpecified) -> Factor:
        """ compute deciles. """
        ...

    def top(self, N:int, mask:Filter|Sentinel=NotSpecified, 
            groupby:Classifier|Sentinel=NotSpecified) -> Filter:
        """ a filter to select the top `N` of the factor. """
        ...

    def bottom(self, N:int, mask:Filter|Sentinel=NotSpecified, 
            groupby:Classifier|Sentinel=NotSpecified) -> Filter:
        """ a filter to select the bottom `N` of the factor. """
        ...

    def percentile_between(self, min_percentile:float, max_percentile:float,
                           mask:Filter|Sentinel=NotSpecified) -> Filter:
        """ filter between the specified percetile values. """
        ...

    def isnan(self) -> Filter:
        """ filter to check if NaN. """
        ...

    def notnan(self) -> Filter:
        """ filter to check if **not** NaN. """
        ...

    def isfinite(self) -> Filter:
        """ filter to check if isfinite. """
        ...

    def clip(self, min_bound:float, max_bound:float, 
             mask:Filter|Sentinel=NotSpecified) -> Factor:
        """ clip the values between the bounds. """
        ...

class CustomFactor(Factor):
    inputs:list[BoundColumn]
    outputs:list[str]
    window_length:int|Sentinel=NotSpecified
    mask:Filter|Sentinel=NotSpecified

    def compute(self, today:pandas.Timestamp, assets:numpy.ndarray, out:numpy.ndarray, 
                *args) -> None:
        """ custom factor computation. """
        ...

class Latest(CustomFactor):
    """ latest value. """
    ...
