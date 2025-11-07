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
from typing import Callable
from blueshift.assets import MarketData
from blueshift.types import AlgoContext, Asset
from blueshift.pipeline.filters import Filter
from blueshift.pipeline.factors import Factor

def select_universe(lookback:int, size:int, context:AlgoContext|None=None) ->Filter:
    """returns a filter for average dollar volume based on `lookback`, selecting top `size` assets."""
    ...

def average_volume_filter(lookback:int, amount:float, context:AlgoContext|None=None) -> Filter:
    """returns a filter for average dollar volume based on `lookback`, selecting values > `amount`."""
    ...

def filter_assets(func:Callable[[Asset], bool], context=None) -> Filter:
    """select assets with user-defined `func` that takes in an asset and returs True to select. """
    ...

def filter_universe(universe:list[Asset], context:AlgoContext|None=None) -> Filter:
    """ filter based on user-supplied list of assets. """
    ...

def exclude_assets(universe:list[Asset], context:AlgoContext|None=None) -> Filter:
    """ filter based by excluding user-supplied list of assets. """
    ...

def returns_factor(lookback:int, offset:int=0, context:AlgoContext|None=None) -> Factor:
    """returns over `lookback` with an `offset`. """
    ...

def period_returns(lookback:int, offset:int=0, context:AlgoContext|None=None) -> Factor:
    """returns over `lookback` with an `offset`. """
    ...

def filtered_returns_factor(lookback:int, filter_:Filter, offset:int=0, 
                            context:AlgoContext|None=None) -> Factor:
    """ returns over `lookback` with an `offset` after applying `filter_` filtering. """
    ...

def technical_factor(lookback:int, indicator_fn:Callable, indicator_lookback:int|None=None,
                     context:AlgoContext|None=None, *args, **kwargs) -> Factor:
    """ apply a technical indicator function with window length `lookback`, and lookback `indicator_lookback`. """
    ...

def asset_beta(market:MarketData, lookback:int, context:AlgoContext) -> Factor:
    """ returns beta factor with respect to the `market` asset. """
    ...