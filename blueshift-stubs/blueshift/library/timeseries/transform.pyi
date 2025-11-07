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
from typing import Callable
import pandas

from blueshift.protocol import TradingCalendar

def resample(df:pandas.Series|pandas.DataFrame, period:str, fill_value:float|int|None=None, 
             fill_method:str='ffill', limit:int|None=None, default_func:Callable|str|dict='last', 
             calendar:TradingCalendar|None=None) -> pandas.Series|pandas.DataFrame:
    """ resample pandas dataframe or series. """
    ...

def endpoints(df:pandas.Series|pandas.DataFrame, on:str) -> pandas.DatetimeIndex:
    """get a DatetimeIndex resampled from the input series based on the period specified by on. """
    ...

def split(df:pandas.Series|pandas.DataFrame, on:str) -> list[pandas.Series]|list[pandas.DataFrame]:
    """ split a dataframe by time periods and get a list of data frames. """
    ...

def period_apply(df:pandas.Series|pandas.DataFrame, on:str, 
                 func:str|Callable|dict) -> pandas.Series|pandas.DataFrame:
    """ apply aggregation by periods. """
    ...

def rollapply(df:pandas.Series|pandas.DataFrame, width:int, func:Callable, 
              y:pandas.Series|pandas.DataFrame|None=None, by:int=0, by_column:bool=True, 
              fill:bool=True, partial:bool=False, align:str='right', coredata:bool=False, 
              **kwargs) -> pandas.Series|pandas.DataFrame:
    """ apply a function on a rolling window of size `width`. """
    ...

def cumulative_apply(df:pandas.Series|pandas.DataFrame, func:Callable, min_period:int=1, 
                     by_column:bool=True, fill:bool=True, partial:bool=False, align:str='right', 
                     coredata:bool=False, **kwargs) -> pandas.Series|pandas.DataFrame:
    """ apply a function cumulatively. """
    ...
