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

from .factors import Factor, CustomFactor, Latest
from .basic import (
    AnnualizedVolatility,
    AverageDollarVolume,
    DailyReturns,
    ExponentialWeightedMovingAverage,
    ExponentialWeightedMovingStdDev,
    LinearWeightedMovingAverage,
    MaxDrawdown,
    PeerCount,
    PercentChange,
    Returns,
    SimpleMovingAverage,
    VWAP,
    WeightedAverageValue,
)
from .statistical import (
    RollingPearson,
    RollingSpearman,
    RollingLinearRegressionOfReturns,
    RollingPearsonOfReturns,
    RollingSpearmanOfReturns,
    SimpleBeta,
)
from .technical import (
    Aroon,
    BollingerBands,
    FastStochasticOscillator,
    IchimokuKinkoHyo,
    MACDSignal,
    RateOfChangePercentage,
    RSI,
    TrueRange,
)

__all__ = [
    'AnnualizedVolatility',
    'Aroon',
    'AverageDollarVolume',
    'BollingerBands',
    'CustomFactor',
    'DailyReturns',
    'ExponentialWeightedMovingAverage',
    'ExponentialWeightedMovingStdDev',
    'Factor',
    'FastStochasticOscillator',
    'IchimokuKinkoHyo',
    'Latest',
    'LinearWeightedMovingAverage',
    'MACDSignal',
    'MaxDrawdown',
    'PeerCount',
    'PercentChange',
    'RSI',
    'RateOfChangePercentage',
    'Returns',
    'RollingLinearRegressionOfReturns',
    'RollingPearson',
    'RollingPearsonOfReturns',
    'RollingSpearman',
    'RollingSpearmanOfReturns',
    'SimpleBeta',
    'SimpleMovingAverage',
    'TrueRange',
    'VWAP',
    'WeightedAverageValue',
]