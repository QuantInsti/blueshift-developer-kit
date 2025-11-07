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

from typing import Literal
from enum import Enum
import pandas
import datetime
from .assets import Asset

class ListLike:
    """ Use `isinstance(var, ListLike)` to test if a variable `var` is a non-string iterabele. """
    ...

class GREEK(Enum):
    """ options greek enums. """
    DELTA=0
    GAMMA=1
    VEGA=2
    THETA=3

class AlgoMode(Enum):
    """ algo run mode enums. """
    BACKTEST = 'BACKTEST'
    LIVE = 'LIVE'
    PAPER = 'PAPER'
    EXECUTION = 'EXECUTION'

class ExecutionMode(Enum):
    """ algo order execution mode enums. """
    AUTO = 'AUTO'
    ONECLICK = 'ONECLICK'

class ExitMethod(Enum):
    """ SL/TP exit method enumus. """
    PRICE = 0
    MOVE = 1
    PERCENT = 2
    AMOUNT = 3
    PNL = 4

class ProductType(Enum):
    """ 
        order product type - `INTRADAY` automatically squared-off the same day. 
        `DELIVERY` product requires upfront full cash value, while `MARGIN` products
        requires only a margin to trade.
    """
    INTRADAY = 0
    DELIVERY = 1
    MARGIN = 2

class OrderType(Enum):
    """ order type enums - limit or market order. """
    MARKET = 0
    LIMIT = 1

class OrderValidity(Enum):
    """ supported order validity enum. """
    DAY = 0
    IOC = 1
    FOK = 2

class OrderSide(Enum):
    """ order side enum - buy or sell. """
    BUY = 0
    SELL = 1

class OrderStatus(Enum):
    """ order status enum. """
    COMPLETE = 0
    OPEN = 1
    REJECTED = 2
    CANCELLED = 3

class Order:
    """ Blueshift order object. """
    oid:str
    asset:Asset
    quantity:float
    product_type:ProductType
    order_type:OrderType
    order_validity:OrderValidity
    disclosed:float
    price:float
    trigger_price:float
    stoploss_price:float
    filled:float
    pending:float
    average_price:float
    side:OrderSide
    status:OrderStatus
    timestamp:pandas.Timestamp
    exchange_timestamp:pandas.Timestamp
    fractional:bool
    price_at_entry:float
    create_latency:float
    exec_latency:float

    def to_dict(self) -> dict:
        """ returns a dict representation. """
        ...

    def is_open(self) -> bool:
        """True if the order is open. """
        ...

    def is_done(self) -> bool:
        """True if the order is complete. """
        ...

    def is_cancelled(self) -> bool:
        """True if the order is cancelled. """
        ...

    def is_rejected(self) -> bool:
        """True if the order is rejected. """
        ...

    def is_final(self) -> bool:
        """True if the order is not open anymore (i.e. complete|cancelled|rejected). """
        ...

    def is_buy(self) -> bool:
        """True if the order is compla buy order. """
        ...

class PositionSide(Enum):
    """ position side enum - long or short. """
    LONG = 0
    SHORT = 1

class Position:
    """ Blueshift position object. """
    asset:Asset
    quantity:float
    buy_quantity:float
    buy_price:float
    sell_quantity:float
    sell_price:float
    pnl:float
    realized_pnl:float
    unrealized_pnl:float
    last_price:float
    last_fx:float
    timestamp:pandas.Timestamp
    value:float
    cost_basis:float
    margin:float
    product_type:ProductType
    position_side:PositionSide
    fractional:bool

    def to_dict(self) -> dict:
        """ returns a dict representation. """
        ...

    def if_closed(self)->bool:
        """True if the position is closed out. """
        ...

class TradingCalendar:
    """ Blueshift trading calendar object. """
    name:str
    minutes_per_day:int
    tz:str
    open_time:datetime.time
    close_time:datetime.time

    def to_timestamp(self, dt:str|pandas.Timestamp) -> pandas.Timestamp:
        """ returns timestamp with automatic timezone handling. """
        ...

    def is_session(self, dt:str|pandas.Timestamp) -> bool:
        """ true if `dt` is a valid trading day. """
        ...

    def is_holiday(self, dt:str|pandas.Timestamp) -> bool:
        """ true if `dt` is a trading holiday. """
        ...

    def is_open(self, dt:str|pandas.Timestamp) -> bool:
        """ true if the market is open at `dt`. """
        ...

    def next_open(self, dt:pandas.Timestamp) -> pandas.Timestamp:
        """ returns next trading session open timestamp. """
        ...

    def previous_open(self, dt:pandas.Timestamp) -> pandas.Timestamp:
        """ returns previous trading session open timestamp. """
        ...

    def to_open(self, dt:pandas.Timestamp) -> pandas.Timestamp:
        """ returns current trading session open timestamp. """
        ...

    def next_close(self, dt:pandas.Timestamp) -> pandas.Timestamp:
        """ returns next trading session close timestamp. """
        ...

    def previous_close(self, dt:pandas.Timestamp) -> pandas.Timestamp:
        """ returns previous trading session close timestamp. """
        ...

    def to_close(self, dt:pandas.Timestamp) -> pandas.Timestamp:
        """ returns current trading session close timestamp. """
        ...

    def sessions(self, start_dt:str|pandas.Timestamp, end_dt:str|pandas.Timestamp, convert:bool=True) -> list[pandas.Timestamp]|pandas.DatetimeIndex:
        """ returns all trading session between start and end dates. """
        ...

    def next_session(self, dt:str|pandas.Timestamp) -> pandas.Timestamp:
        """ returns next trading session. """
        ...

    def previous_session(self, dt:str|pandas.Timestamp) -> pandas.Timestamp:
        """ returns previous trading session. """
        ...

    def last_n_sessions(self, dt:str|pandas.Timestamp, n:int, convert:bool=True) -> list[pandas.Timestamp]|pandas.DatetimeIndex:
        """ returns the last `n` sessions. """
        ...

    def next_n_sessions(self, dt:str|pandas.Timestamp, n:int, convert:bool=True) -> list[pandas.Timestamp]|pandas.DatetimeIndex:
        """ returns the next `n` sessions. """
        ...

    def bump_date(self, dt:str|pandas.Timestamp, 
                  bump:Literal['previous','forward','mod_previous','mod_forward']) -> pandas.Timestamp:
        """bump date to a trading session. """
        ...