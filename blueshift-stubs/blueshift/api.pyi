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
import datetime
from .assets import Asset
from .protocol import Order, OrderValidity, Position, ExitMethod
from .finance.commission import CostModel
from .finance.slippage import SlippageModel
from .finance.margin import MarginModel
from .types import AlgoContext, DataPortal
from .pipeline import Pipeline

class EventHandle:
    """event handle returned by scheduling API methods. """
    def cancel(self):
        """cancel the scheduled callback. """
        ...

class date_rules:
    """ date rules for scheduling callbacks. """
    @classmethod
    def everyday(cls):
        """trigger callback every day."""
        ...

    @classmethod
    def on(cls, dts:list[pandas.Timestamp]):
        """ trigger on specific dates. """
        ...

    @classmethod
    def expiry(cls, context:AlgoContext, asset:Asset, days_offset:int=0):
        """trigger `days_offset` before the expiry days. """
        ...

    @classmethod
    def week_start(cls, days_offset=0):
        """trigger `days_offset` after start of the week. """
        ...

    @classmethod
    def week_end(cls, days_offset=0):
        """trigger `days_offset` before end of the week. """
        ...

    @classmethod
    def week_day(cls, weekday:int|list[int]|str|list[str]=0):
        """trigger on specifc day(s) of the week"""
        ...

    @classmethod
    def month_start(cls, days_offset=0):
        """trigger `days_offset` after start of the month. """
        ...

    @classmethod
    def month_end(cls, days_offset=0):
        """trigger `days_offset` before end of the month. """
        ...

class time_rules:
    """time rules for scheduled callbacks. """

    @classmethod
    def at(cls, at:str|datetime.time):
        """trigger at a specific time."""
        ...

    @classmethod
    def market_open(cls, minutes:int=0, hours:int=0):
        """trigger specified hours and minutes after market open. """
        ...

    @classmethod
    def market_close(cls, minutes:int=2, hours:int=0):
        """trigger specified hours and minutes before market close. """
        ...

    @classmethod
    def every_nth_minute(cls, n:int=0):
        """trigger every n-th minute starting at market open. """
        ...

    @classmethod
    def every_minute(cls):
        """trigger every minute starting at market open. """
        ...

    @classmethod
    def every_nth_hour(cls, n=0):
        """trigger every n-th hours starting at market open. """
        ...

    @classmethod
    def every_hour(cls):
        """trigger every hour starting at market open. """
        ...

def log_info(msg:str) -> None:
    """log a message. """
    ...

def log_warning(msg:str) -> None:
    """log a message as warning. """
    ...

def log_error(msg:str) -> None:
    """log a message as error. """
    ...

def symbol(symbol_str: str, dt: pandas.Timestamp | None = None, *args, **kwargs) -> Asset:
    """
        API function to resolve a symbol string to an asset.

        Symbology:
            Use symbol('TICKER') for equities, indices and ETFs. 
            
            Use symbol('UNDERLYINGY{YYYMMDD}FUT') for futures with a specific expiry. 
            Use symbol('UNDERLYINGY-{EXP}') for rolling futures - where EXP is `I` for first month, 
            `II` for second month etc.
            
            Use symbol('UNDERLYINGY{YYYMMDD}CE{STRIKE}') for options with specific expiry 
            and strike. Use symbol('UNDERLYINGY-{EXP}{TYPE}{K}') for rolling options. In 
            this case `EXP` can be `W0` for first weekly, `W1` for next week so on, and 
            `I` for first monthly, `II` for next month and so on. TYPE can be either `CE`
            (call) or `PE` (put). The strike specification K can be either based on offset 
            from ATM (e.g. +0 for ATM, +100 for ATM+100 etc.), or number of strikes away from 
            ATM (e.g. 2OTM means 2 strikes away out of the money, 3ITM mean 3 strikes away 
            in the money etc.), or based on delta (e.g. +25D means 0.25 delta) or price in 
            cents (500P means strike such that option price is nearest to 5 dollar). You can 
            also specify an extra keyword arguments `use_spot` for rolling option to select 
            strikes relative to underlying spot prices (otherwise defaults to futures prices.)

            Use symbol('BASE/QUOTE') for forex like assets (e.g. currencies and crpytos). For 
            example, use symbol('BTC/USD') for Bitcoin quoted in US dollars.
    """
    ...

def create_order(asset:Asset, quantity:float, limit_price:float=0, 
                 validity: OrderValidity | str = 'day', **kwargs) -> Order:
    """ create an order object. Use a non-zero `limit_price` for a limit order. """
    ...

def order(asset:Asset|Order|list[Order], quantity:float | None = None, limit_price:float=0, 
          validity: OrderValidity | str = 'day', **kwargs) -> list[str]|str:
    """
        place an order. quantity is reqiured if the first argument is `Asset`.
        Use a non-zero `limit_price` for a limit order. Parameters like `quantity`,
        `limit_price`, `validity` etc will be ignored if the first argument is an 
        `Order` object or a list of such objects.
    """
    ...

def order_percent(asset:Asset, quantity:float, limit_price:float=0, 
                  validity: OrderValidity | str = 'day', **kwargs) -> list[str]|str:
    """place an order for an asset with fraction of the account net worth. """
    ...

def order_value(asset:Asset, quantity:float, limit_price:float=0, 
                validity: OrderValidity | str = 'day', **kwargs) -> list[str]|str:
    """place an order for an asset with the specified dollar value. """
    ...

def order_target(asset:Asset, quantity:int, limit_price:float=0, 
                 validity: OrderValidity | str = 'day', **kwargs) -> list[str]|str:
    """place an order for an asset for a target quantity. """
    ...

def order_target_percent(asset:Asset, quantity:float, limit_price:float=0, 
                         validity: OrderValidity | str = 'day', **kwargs) -> list[str]|str:
    """place an order for an asset with a traget of portfolio fraction. """
    ...

def order_target_value(asset:Asset, quantity:float, limit_price:float=0, 
                       validity: OrderValidity | str = 'day', **kwargs) -> list[str]|str:
    """place an order for an asset with a traget of dollar value. """
    ...

def order_with_retry(asset:Asset, quantity:int, max_retries:float=3, 
                     limit_price:float=0, **kwargs) -> list[str]:
    """place an IOC order for a given quantity with automatic retries, and wait for execution. """
    ...

def update_order(order_param:str | Order, *args, **kwargs) -> str:
    """ update an open order. """
    ...

def cancel_order(order_param:str | Order, *args, **kwargs) -> str:
    """ cancel an open order. """
    ...

def wait_for_trade(order_ids:list[str], timeout:float=1, exit_time:bool=False) -> None:
    """ wait for the orders to execute. """
    ...

def wait_for_exit(assets:list[Asset]|None=None, check_orders:bool=True, check_positions:bool=True, 
                  timeout:float=1) -> None:
    """ wait for algo to exit after all positions are exited and/or open orders are cancelled. """
    ...

def square_off(assets:Asset|list[Asset]|None=None, ioc:bool=False, 
               remark:str|None=None, **kwargs) -> bool:
    """square-off existing positions. If the first argument is `None` all positions will be squared off. """
    ...

def set_stoploss(asset:Asset|None, method:str|ExitMethod, target:float, trailing:bool=False, 
                 on_stoploss:Callable[[AlgoContext, Asset|None], None]|None=None, 
                 skip_exit:bool=False, entry:float|None=None) -> None:
    """ 
        Set a position (`Asset`) or strategy(`None`) wise stoploss with optional callback. 
        Define `on_stoploss` globally, or pass a callable to run on stoploss hit. Set 
        `skip_exit` to True to skip position exit.
    """
    ...

def get_current_stoploss(asset:Asset|None) -> tuple[ExitMethod, float, float]:
    """ get the current stoploss details. """
    ...

def remove_stoploss(asset:Asset|None) -> None:
    """ remove the current stoploss. """
    ...

def set_takeprofit(asset:Asset|None, method:str|ExitMethod, target:float, 
                   on_takeprofit:Callable[[AlgoContext, Asset|None], None]|None=None, 
                   skip_exit:bool=False, entry:float|None=None) -> None:
    """ 
        Set a position (`Asset`) or strategy(`None`) wise take-profit target with optional callback. 
        Define `on_takeprofit` globally, or pass a callable to run on take-profit hit. Set 
        `skip_exit` to True to skip position exit.
    """
    ...

def get_current_takeprofit(asset:Asset|None) -> tuple[ExitMethod, float, float]:
    """ get the current takeprofit details. """
    ...

def remove_takeprofit(asset:Asset|None) -> None:
    """ remove the current takeprofit target. """
    ...

def get_open_orders() -> dict[str, Order]:
    """ get open orders as a dictionary. """
    ...

def get_open_positions() -> dict[Asset, Position]:
    """ get open positions as a dictionary. """
    ...

def get_order(order_id:str) -> Order|None:
    """ get order by order ID. """
    ...

def set_exit_policy(cancel_orders:bool=True, square_off:bool=False) -> None:
    """ set exit policy. Setting `square_off` to True also means `cancel_orders` is True. """
    ...

def set_cooloff_period(period:float=30) -> None:
    """ set strategy exit cool-off period. """
    ...

def get_cooloff_period() -> float:
    """ get the current exit cool-off period. """
    ...

def set_cooloff() -> None:
    """ trigger an exit cool-off. """
    ...

def reset_cooloff() -> None:
    """ turn-off all exit cool-off. """
    ...

def terminate(error:str|None=None, cancel_orders:bool=True, is_error:bool=False) -> None:
    """ stop algo run immediately - useful for error handling. """
    ...

def finish(msg:str|None=None) -> None:
    """ schedule algo exit. """
    ...

def attach_pipeline(pipeline:Pipeline, name:str) -> None:
    """ register a pipeline with the algo. """
    ...

def pipeline_output(name:str) -> pandas.DataFrame:
    """ fetch the pipeline output for the current timestamp. """
    ...

def set_slippage(model:SlippageModel, *args, **kwargs) -> None:
    """ set the simulation slippage model"""
    ...

def set_commission(model:CostModel, *args, **kwargs) -> None:
    """ set the simulation commission model"""
    ...

def set_margin(model:MarginModel, *args, **kwargs) -> None:
    """ set the simulation commission model"""
    ...

def get_datetime() -> pandas.Timestamp:
    """ get the current timestamp (tz-aware). """
    ...

def record(*args, **kwargs) -> None:
    """ record a metric. Note: only one observation (latest call to this function) is recorded per day. """
    ...

def record_state(state:str) -> None:
    """ 
        record a user-defined state. This markes the named state (say "my_state") attribute of the context 
        variable (`context.my_state` must be defined) for automatic persistance and can be loaded in 
        the next run using `load_state`. Also, my_state must be json serializable with size restrictions.
    """
    ...

def load_state() -> None:
    """ load user-defined state as context variable - saved previously using `record_state`. """
    ...

def fund_transfer(amount:float, *args, **kwargs) -> None:
    """ 
        transfer a given amount to strategy virtual account. This does NOT transfer actual fund, 
        but impacts performance metrics calculations that relies on deployed capital.
    """
    ...

def set_benchmark(asset:Asset) -> None:
    """set an Asset as strategy benchmark. """
    ...

def set_algo_parameters(param_name:str='params') -> None:
    """ set the context variable attribute name that will be treated as strategy parameters. """
    ...

def set_initial_positions(positions:list[Position]|list[dict]) -> None:
    """ set the initial position for the algo. """
    ...

def exit_when_done(completion_msg:str|None=None, check_orders:bool=True, check_positions:bool=False, 
                   timeout:float|None=None) -> None:
    """exit positions and/or cancel open orders and exit from current algo. """
    ...

def schedule_order_callback(callback:Callable[[AlgoContext, list[str]], None], order_ids:list[str], timeout:float=1, 
                            on_timeout:Callable[[AlgoContext, list[str]], None]|None=None) -> EventHandle:
    """ schedule a callable f(context, order_ids) once ALL the orders are not open anymore. """
    ...

def schedule_soon(callback:Callable[[AlgoContext, DataPortal], None]) -> EventHandle:
    """ schedule a callback to be called as soon as in trading session. """
    ...

def schedule_once(callback:Callable[[AlgoContext, DataPortal], None]) -> EventHandle:
    """ schedule a callback to be called in the next clock cycle. """
    ...

def schedule_later(callback:Callable[[AlgoContext, DataPortal], None], delay:float) -> EventHandle:
    """ schedule a callback to be called after a delay. """
    ...

def schedule_at(callback:Callable[[AlgoContext, DataPortal], None], at:datetime.time|str) -> EventHandle:
    """ schedule a callback to be called at a given time in the current trading session. """
    ...

def schedule_function(callback:Callable[[AlgoContext, DataPortal], None], 
                      date_rule:date_rules|None=None, time_rule:time_rules|None=None) -> EventHandle:
    """ schedule a callback to be called at a given time in the current trading session. """
    ...

