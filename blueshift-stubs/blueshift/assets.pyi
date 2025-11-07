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

from enum import Enum
import pandas

class AssetClass(Enum):
    EQUITY = 0
    FOREX = 1

class InstrumentType(Enum):
    SPOT = 0
    FUTURES = 1
    OPT = 2
    MARGIN = 3
    FUNDS = 4

class OptionType(Enum):
    CALL = 0
    PUT = 1

class StrikeType(Enum):
    ABS = 0
    REL = 1

class MarketData:
    symbol:str
    name:str
    start_date:pandas.Timestamp
    end_date:pandas.Timestamp
    exchange_name:str
    calendar_name:str
    ...

class Asset(MarketData):
    asset_class:AssetClass
    instrument_type:InstrumentType
    mult:float
    tick_size:int
    auto_close_date:pandas.Timestamp
    can_trade:bool
    fractional:bool

    def to_dict(self) -> dict:
        """ returns a dict representation. """
        ...

    def is_futures(self) -> bool:
        """True if an futures instrument. """
        ...
    
    def is_opt(self) -> bool:
        """True if an option instrument. """
        ...

    def is_rolling(self) -> bool:
        """True if an futures/option instrument created with rolling symbol. """
        ...
    ...

class Equity(Asset):
    shortable:bool
    borrow_cost:bool
    ...

class EquityIntraday(Equity):
    ...

class EquityMargin(Equity):
    ...

class EquityFutures(Equity):
    underlying:str
    roll_day:int
    expiry_date:pandas.Timestamp
    initial_margin:float
    maintenance_margin:float
    ...

class EquityOption(EquityFutures):
    strike:float
    strike_type:StrikeType
    option_type:OptionType
    ...

class Forex(Asset):
    ccy_pair:str
    base_ccy:str
    quote_ccy:str
    buy_roll:float
    sell_roll:float
    initial_margin:float
    maintenance_margin:float
    ...