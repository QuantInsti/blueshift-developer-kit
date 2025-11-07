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

class SlippageModel:
    """ abstract slippage model. """
    ...

class NoSlippage(SlippageModel):
    def __init__(self, max_volume:float=0.02):
        """ 
            No slippage model, set `max_volume` to zero to remove volume limit. 

            Args:
                max_volume: maximum participation (fraction of volume traded at the bar that can be filled).
        """
        ...

class BidAskSlippage(SlippageModel):
    def __init__(self, max_volume:float=0.02):
        """ 
            Bid-ask based slippage model, set `max_volume` to zero to remove volume limit. 
            Will raise error if the underlying dataset does not support bid-ask prices.

            Args:
                max_volume: maximum participation (fraction of volume traded at the bar that can be filled).
        """
        ...

class VolumeSlippage(SlippageModel):
    def __init__(self, max_volume:float=0.02, cost_coeff:float=0.002, cost_exponent:float=0.5, 
                 spread:float=0.001, spread_is_percentage:bool=True, volume_is_absolute:bool=False, 
                 use_vol:bool=False, vol_floor:float=0.05):
        """ 
            Volume based slippage model. Modeled as participation raised to cost exponent and then 
            multiplied by the cost coefficient and volatility, plus half the spread.

            Args:
                max_volume: maximum participation (fraction of volume traded at the bar that can be filled).
                cost_coeff: cost coefficient.
                cost_exponent: cost exponent.
                spread: constant spread
                spread_is_percentage: If false, spread is treated as absolute
                use_vol: If false, volatility is set to 1.0.
                vol_floor: Floor value of volatility, ignored if use_vol is False.
        """
        ...

class FixedSlippage(VolumeSlippage):
    def __init__(self, spread=0, max_volume=0.02):
        """ 
            Slippage based on a fixed absolute spread. 

            Args:
                spread: constant spread
                max_volume: maximum participation (fraction of volume traded at the bar that can be filled).
        """