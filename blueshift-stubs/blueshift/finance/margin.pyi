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

class MarginModel:
    """ Abstract margin model. """
    ...

class NoMargin(MarginModel):
    def __init__(self) -> None: 
        """No commission charged."""
        ...
    ...

class FlatMargin(MarginModel):
    def __init__(self, intial_margin:float=0.10, maintenance_margin:float|None=None) -> None:
        """
            Margin as a flat percentage of exposure.

            Args:
                intial_margin: margin rate for new orders.
                maintenance_margin: margin rate for overnight positions.
        """
        ...
    ...

