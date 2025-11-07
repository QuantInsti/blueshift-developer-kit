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

class CostModel:
    """ Abstract cost/ commission model. """
    ...

class NoCommission(CostModel):
    def __init__(self) -> None: 
        """No commission charged."""
        ...
    ...

class PerDollar(CostModel):
    def __init__(self, commissions:float=0, cost_cap:float=1E6, cost_floor:float=0, 
                 cost_on_sell_only:bool=False) -> None:
        """
            Commission charged per dollar (traded value).

            Args:
                commissions: per dollar commission charge.
                cost_cap: Max possible brokerage.
                cost_floor: Minimum brokerage levied.
                cost_on_sell_only: If brokerage only on sell leg.
        """
        ...
    ...

class PerShare(CostModel):
    def __init__(self, commissions:float=0, cost_cap:float=1E6, cost_floor:float=0, 
                 cost_on_sell_only:bool=False) -> None:
        """
            Commission charged per share (unit).

            Args:
                commissions: per share commission charge.
                cost_cap: Max possible brokerage.
                cost_floor: Minimum brokerage levied.
                cost_on_sell_only: If brokerage only on sell leg.
        """
        ...
    ...

class PerOrder(CostModel):
    def __init__(self, commissions:float=0, cost_cap:float=1E6, cost_floor:float=0, 
                 cost_on_sell_only:bool=False) -> None:
        """
            Commission charged per order.

            Args:
                commissions: per order commission charge.
                cost_cap: Max possible brokerage.
                cost_floor: Minimum brokerage levied.
                cost_on_sell_only: If brokerage only on sell leg.
        """
        ...
    ...

