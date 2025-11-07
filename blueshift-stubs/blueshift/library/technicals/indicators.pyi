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
from typing import Tuple
import pandas
import numpy

def ma_xover(data:pandas.Series|numpy.ndarray, ltma:int=20, stma:int=5, 
             **kwargs) -> float:
    """ simple moving Average cross-over """
    ...

def MA_XOVER(data:pandas.Series|numpy.ndarray, ltma:int=20, stma:int=5, 
             **kwargs) -> pandas.Series|numpy.ndarray:
    """ vectorized simple moving Average cross-over """
    ...

def ema_xover(data:pandas.Series|numpy.ndarray, ltma:int=20, stma:int=5, 
              **kwargs) -> float:
    """ exponential moving Average cross-over """
    ...

def EMA_XOVER(data:pandas.Series|numpy.ndarray, ltma:int=20, stma:int=5, 
              **kwargs) -> pandas.Series|numpy.ndarray:
    """ vectorized exponential moving Average cross-over """
    ...

def bollinger_band_dist(data:pandas.Series|numpy.ndarray, timeperiod:int=20, 
                        **kwargs) -> float:
    """ normalized distance from uppper bollinger band. """
    ...

def BOLLINGER_BAND_DIST(data:pandas.Series|numpy.ndarray, timeperiod:int=20, 
                        **kwargs) -> pandas.Series|numpy.ndarray:
    """ vectorized normalized distance from uppper bollinger band. """
    ...

def HEIKIN_ASHI(price:pandas.DataFrame, precision:float=2) -> pandas.DataFrame:
    """ Heikin Ashi OHLC(V) from input OHLC(V) price data. """
    ...

def ICHIMOKU_CLOUD(price:pandas.DataFrame, timeperiod1:int=20, timeperiod2:int=60, 
                   timeperiod3:int=120, timeperiod4:int=120) -> pandas.DataFrame:
    """ Ichimoku Cloud """
    ...

def trend_stall(price:pandas.DataFrame, bandwidth:int=5, timeperiod:int=14, sigma:float=1, 
                threshold:float=0.001) -> float:
    """ trend stall signal from input HLC price data. """
    ...

def TREND_STALL(price:pandas.DataFrame, bandwidth:int=5, timeperiod:int=14, sigma:float=1, 
                threshold:float=0.001) -> pandas.Series:
    """ vectorized trend stall signal from input HLC price data. """
    ...

def trend_set(price:pandas.DataFrame, bandwidth:int=5, timeperiod:int=14, sigma:float=1, 
                threshold:float=0.001) -> float:
    """ trend onset signal from input HLC price data. """
    ...

def TREND_SET(price:pandas.DataFrame, bandwidth:int=5, timeperiod:int=14, sigma:float=1, 
                threshold:float=0.001) -> pandas.Series:
    """ vectorized trend onset signal from input HLC price data. """
    ...

def super_trend(price:pandas.DataFrame, timeperiod:int=10, 
                mult:float=3) -> Tuple[float, float, float]:
    """ super trend upper, lower and signal. """
    ...

def SUPER_TREND(price:pandas.DataFrame, timeperiod:int=10, 
                mult:float=3) -> Tuple[pandas.Series, pandas.Series, pandas.Series]:
    """ vectorized super trend upper, lower and signal. """
    ...

