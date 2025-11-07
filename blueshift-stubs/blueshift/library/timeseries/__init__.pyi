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
import numpy
from statsmodels.tsa.arima.model import ARIMA

from blueshift.protocol import TradingCalendar

def intraday_seasonality_func(series:pandas.Timestamp, period:str|None=None, 
                              calendar:TradingCalendar|None=None, bandwidth:float=1.0, 
                              infer_frequency:bool=True, 
                              drop_first_minute:bool=True) -> Callable[[pandas.DatetimeIndex],pandas.Series]:
    """generate the intraday seasonality function. """
    ...

def deseasonalize(series:pandas.Series, seasonality_func:Callable[[pandas.DatetimeIndex],pandas.Series], 
                  period:str, minutes_per_day:int|None=None, 
                  calendar:TradingCalendar|None=None) -> pandas.Series:
    """ deseasonalize an input series. """
    ...

def reseasonalize(series:pandas.Series, seasonality_func:Callable[[pandas.DatetimeIndex],pandas.Series], 
                  period:str, calendar:TradingCalendar) -> pandas.Series:
    """ re-seasonalize an input series. """
    ...

def auto_arima(series, max_terms=5) -> ARIMA:
    """ generate an auto-arima model. """
    ...

class OnlineAutoARIMA:
    model:ARIMA

    def __init__(self, max_coeffs:float=5, period:str|None=None, calendar:TradingCalendar|None=None):
        """ online auto-armia model. """
        ...
    
    def fit(self, data:numpy.ndarray|pandas.DataFrame|pandas.Series) -> None:
        """ initial fit with data. """
        ...

    def update(self, data:numpy.ndarray|pandas.DataFrame|pandas.Series, refit:bool=False) ->None:
        """ online update with new data. """
        ...

    def predict(self, steps:int|None=None) -> numpy.ndarray|pandas.DataFrame|pandas.Series:
        """ predict from the current fitted model. """
        ...

    def transform(self, data:numpy.ndarray|pandas.DataFrame|pandas.Series) -> None:
        """ transfor (does nothing). """
        ...

    def score(self, X:numpy.ndarray|pandas.DataFrame|pandas.Series|None=None, 
              y:numpy.ndarray|pandas.DataFrame|pandas.Series|None=None) -> float:
        """ score the model (returns SSE). """
        ...