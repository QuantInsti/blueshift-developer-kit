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

from typing import Literal, overload
import pandas
from .assets import Asset as Asset
from .protocol import Order, Position, AlgoMode, ExecutionMode, TradingCalendar

class IPortfolio:
    """ Blueshift portfolio object interface. """
    portfolio_value:float
    positions_exposure:float
    cash:float
    starting_cash:float
    returns:float
    positions_value:float
    pnls:float
    mtm:float
    start_date:pandas.Timestamp
    positions:dict[Asset, Position]

class IAccount:
    """ Blueshift account object interface. """
    margin:float
    leverage:float
    gross_leverage:float
    net_leverage:float
    gross_exposure:float
    long_exposure:float
    short_exposure:float
    long_count:int
    short_count:int
    net_exposure:float
    net_liquidation:float
    commissions:float
    charges:float
    total_positions_exposure:float
    available_funds:float
    total_positions_value:float

class AlgoContext:
    """ current algo context, and placeholder for user defined variables. """
    name:str
    mode:AlgoMode
    is_disconnected:bool
    execution_mode:ExecutionMode
    trading_calendar:TradingCalendar
    record_vars:pandas.DataFrame
    pnls:pandas.DataFrame
    orders:dict[str, Order]
    open_orders:dict[str, Order]
    open_orders_by_asset:dict[str, Order]
    blotter_account:dict
    account:IAccount
    portfolio:IPortfolio
    data_portal:DataPortal
    
class DataPortal:
    """Data portal object for historical data query. """
    
    @overload
    def current(self, asset:Asset, columns:str) -> float:
        """Method for fetching latest price data (float). """
        ...

    @overload
    def current(self, asset:list[Asset], columns:str) -> pandas.Series:
        """Method for fetching latest price data (series with assets in index). """
        ...

    @overload
    def current(self, asset:Asset, columns:list[str]) -> pandas.Series:
        """Method for fetching latest price data (series with columns in index). """
        ...

    @overload
    def current(self, asset:list[Asset], columns:list[str]) -> pandas.DataFrame:
        """Method for fetching latest price data (dataframe with assets in index and columns in columns). """
        ...

    @overload
    def history(self, asset:Asset, columns:str, nbars:int, frequency:str) -> pandas.Series:
        """Method for fetching historical price data. Returns series with timestamp in index. """
        ...

    @overload
    def history(self, asset:list[Asset], columns:str, nbars:int, frequency:str) -> pandas.DataFrame:
        """Method for fetching historical price data. Returns frame with timestamp in index, asset in columns."""
        ...

    @overload
    def history(self, asset:Asset, columns:list[str], nbars:int, frequency:str) -> pandas.DataFrame:
        """Method for fetching historical price data. Returns frame with timestamp in index, columns in columns."""
        ...

    @overload
    def history(self, asset:list[Asset], columns:list[str], nbars:int, frequency:str) -> pandas.DataFrame:
        """Method for fetching historical price data. Returns multi-index frame with asset as level 0 and timestamp as level 1in index, columns in columns."""
        ...

    def fundamentals(self, asset:Asset| list[Asset], metrics:str| list[str], nbars:int, frequency:str) -> dict:
        """Method for fetching corporate fundamental data. Returns dict keyed by asset and frame for as value with metrics in columns. """
        ...
    
    def subscribe(self, asset:Asset| list[Asset], level: Literal[1, 2] = 1, *args, **kwargs) -> None:
        """ subscribe to streaming price data. """
        ...

    def unsubscribe(self, asset:Asset| list[Asset], level: Literal[1, 2] = 1, *args, **kwargs) -> None:
        """ unsubscribe from streaming priec data. """
        ...
    