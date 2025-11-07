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
from blueshift.lib.common.sentinels import NotSpecified, Sentinel

from .factors import CustomFactor, Factor
from ..data import BoundColumn, EquityPricing

class RSI(CustomFactor):
    """ rsi factor. """
    def __init__(self, inputs:list[BoundColumn|Factor]=[EquityPricing.close], 
                 window_legth:int=15) -> None: ...
    ...

class BollingerBands(CustomFactor):
    """ bollinger band factor. """
    lower:Factor
    upper:Factor
    middle:Factor

    def __init__(self, inputs:list[BoundColumn|Factor]=[EquityPricing.close], 
                 window_legth:int|Sentinel=NotSpecified, k:float|Sentinel=NotSpecified) -> None: ...
    ...

class Aroon(CustomFactor):
    """ aroom indicator. """
    down:Factor
    up:Factor

    def __init__(self, inputs:list[BoundColumn|Factor]=[EquityPricing.high, EquityPricing.low], 
                 window_length:int|Sentinel=NotSpecified) -> None: ...
    ...

class FastStochasticOscillator(CustomFactor):
    """ fast stochastic oscillator. """
    def __init__(self, inputs:list[BoundColumn|Factor]=[EquityPricing.close, EquityPricing.low, EquityPricing.high], 
                 window_legth:int=14) -> None: ...
    ...

class IchimokuKinkoHyo(CustomFactor):
    """Ichimoku Cloud factor. """
    tenkan_sen:Factor
    kijun_sen:Factor
    senkou_span_a:Factor
    senkou_span_b:Factor
    chikou_span:Factor

    def __init__(self, inputs:list[BoundColumn|Factor]=[EquityPricing.high, EquityPricing.low, EquityPricing.close], 
                 window_legth:int=52, tenkan_sen_length:int=9, kijun_sen_length:int=26, 
                 chikou_span_length:int=26) -> None: ...
    ...

class RateOfChangePercentage(CustomFactor):
    """ ROC factor. """
    def __init__(self, inputs:list[BoundColumn]=[EquityPricing.close], 
                 window_legth:int|Sentinel=NotSpecified) -> None: ...
    ...

class TrueRange(CustomFactor):
    """ True Range factor. """
    def __init__(self, inputs:list[BoundColumn|Factor]=[EquityPricing.high, EquityPricing.low, EquityPricing.close], 
                 window_legth:int=2) -> None: ...
    ...

class MACDSignal(CustomFactor):
    """ MACD signal factor. """
    def __init__(self, inputs:list[BoundColumn]=[EquityPricing.close], 
                 fast_period:int=12,  slow_period:int=26, signal_period:int=9) -> None: ...
    ...