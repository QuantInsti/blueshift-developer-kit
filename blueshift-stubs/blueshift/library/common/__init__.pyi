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
from enum import Enum
from typing import Any
import pandas

from blueshift.types import AlgoContext, Asset
from blueshift.protocol import ProductType

def str2bool(value:str|bool) -> bool:
    """ convert a string to bool. """
    ...

def get_upfront_capital(context:AlgoContext, asset:Asset, quantity:float, 
                        product_type:ProductType|None=None, pct_margin:float=0.15) -> float:
    """ return upfrom capital required for a position. """
    ...

class Signal(Enum):
    """ an Enum for trading signal. """
    LONG_ENTRY:Any
    LONG_ENTRY_STRONG:Any
    SHORT_ENTRY:Any
    SHORT_ENTRY_STRONG:Any
    LONG_EXIT:Any
    SHORT_EXIT:Any
    EXIT:Any
    NO_SIGNAL:Any

class LineType(Enum):
    """ an Enum for line types from `find_support_resistance`|`find_trends`"""
    SUPPORT:Any
    RESISTANCE:Any
    TREND:Any
    VARIANCE:Any

class Line:
    """ line object from `find_support_resistance`|`find_trends`"""
    type:LineType
    line:pandas.Series
    slope:float
    intercept:float
    score:float

    def is_breakout(self, level:float, dt:pandas.Timestamp) -> bool:
        """ check if we have a breakout. """
        ...

    def get_level(self, dt:pandas.Timestamp) -> float:
        """ get interpolated/ extrapolated level for the timestamp. """
        ...

    def to_support(self) -> None:
        """ set linetype as `support`. """
        ...

    def to_resistance(self) -> None:
        """ set linetype as `resistance`. """
        ...

    def plot(self)->None:
        """ plot the line. """
        ...

class Pattern:
    """A class to capture important points based patterns."""
    name:str
    points:pandas.Series
    lines:list[Line]
    level:float
    aspect:float

    def plot(self)->None:
        """ plot the pattern. """
        ...
