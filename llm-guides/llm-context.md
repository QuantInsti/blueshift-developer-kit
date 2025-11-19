---
title: Blueshift LLM Strategy Developer Guide
version: 1.0
framework: blueshift
purpose: |
  This guide enables large language models (e.g., ChatGPT) to generate accurate Python strategy code 
  using the Blueshift backtesting and live trading API when the user describes trading logic in natural language. This can also be used to debug existing strategies written for Blueshift.

usage_instructions:
  - Import the type definition module for code autocomplete: `from blueshift.types import *` at the start of the strategy code. It is not an error if not used, but a recommendation.
  - Always import necessary modules from blueshift.api, or otherwise specified module
  - Every strategy must define `initialize(context:AlgoContext)` function.
  - Use `schedule_funtion` only inside `initialize`.
  - Do not use `schedule_later` inside `initialize` or `before_trading_start`.
  - Use Blueshift API functions such as `order_target`, and `schedule_function` as shown in examples.
  - Define all user created variables as attribute of the `context` variable as show in the examples. Avoid defining global variables.
  - Do not use underscore (`_`) as the leading or trailing character of a variable function name
  - Use only the whitelisted Python packages if required, do not use unsupported packages or libraries.
  - Use `print` or `log_info` sparingly. If really required, prefer `log_info` over `print`.
  - Generate concise and readable code.
  - Follow the structure and coding style in this document.

expected_behavior:
  - When the user describes a trading idea, generate complete Python code that runs on the Blueshift platform.
  - Follow naming conventions and best practices from this guide.
  - Always ensure code compiles and uses correct API calls.

example_usage_prompt: |
  "Using the uploaded Blueshift LLM Strategy Developer Guide, write a strategy that buys when 
   the 10-day moving average crosses above the 30-day moving average and sells when it crosses below."

last_updated: 2025-11-01
compatible_blueshift_version: ">=5.0.0"
---

# Blueshift Trading Strategy Developer Guide (LLM Context)

## Table of Contents

- [1. Overview & Core Concepts](#1-overview--core-concepts)
  - [Key Components of a Strategy](#key-components-of-a-strategy)
- [2. Strategy Code Examples](#2-strategy-code-examples)
  - [2.1 Example 1: Moving Average Crossover](#21-example-1-moving-average-crossover)
  - [2.2 Example 2: Intraday Short Straddle](#22-example-2-intraday-short-straddle)
- [3. API Reference](#4-api-reference)
  - [3.1. Core Event Callback Functions](#31-core-event-callback-functions)
  - [3.2. Context Object (`context`)](#32-context-object-context)
  - [3.3. Data Object (`data`)](#33-data-object-data)
  - [3.4. The `symbol` API Function and Asset Symbol Format](#34-the-symbol-api-function-and-asset-symbol-format)
  - [3.5. Scheduling Functions and Rules](#35-scheduling-functions-and-rules)
  - [3.6. Order Functions](#36-order-functions)
  - [3.7. Stoploss and Risk Management APIs](#37-stoploss-and-risk-management-apis)
  - [3.8. Asset, Order and Position Objects](#38-asset-order-and-position-objects)
  - [3.9. Slippage and Cost Simulation APIs](#39-slippage-and-cost-simulation-apis)
  - [3.10. Algo State Management](#310-algo-state-management)
- [4. Whitelisted Python packages](#4-whitelisted-python-packages)
- [5. Best Practices](#5-best-practices)

---

## 1. Overview & Core Concepts

This document provides the necessary information for an AI assistant to generate Python code for the Blueshift algorithmic trading library.

The Blueshift framework is **event-driven**. This is the most important concept. You do not write a script that runs from top to bottom. Instead, you define some specific functions (callbacks) that the framework calls when certain events happen (e.g., a new bar of data arrives, an order is filled). Trading related actions (e.g. fetching data and placing orders etc.) happen through a comprehensive set of API functions. These API functions can only be used from within the callback functions or functions invoked by them.

### Key Components of a Strategy:

*   **Callbacks:** Functions you implement in your strategy that respond to pre-defined events (e.g., `def initialize(context):`, `before_trading_start(context, data)` or `handle_data(context, data)`).
*   **Context:** A persistent Python object (`context:AlgoContext`) that holds state between event calls. You use it to query algo state (e.g. open orders or portfolio holdings) or store variables like your indicators, trackers or any other data your strategy needs to track.
*   **Data:** An object (`data:DataPortal`) passed to most callback and scheduled functions that provides access to current and historical market data for all assets in your universe.
*   **API functions** A set of python functions that enables trading related actions (e.g. `symbol` to fetch an asset instrument by ticker, `order` for placing trades, `square_off` to exit positions etc.)

---

## 2. Strategy Code Examples

### 2.1. Example 1: Moving Average Crossover

This is a complete, functional example of a common trading strategy. It demonstrates 

- repeated signal check using `schedule_function` API.
- defining and accepting external parameters using `set_algo_parameters` and `context.params` object.
- how to use historical data, calculate indicators, and place orders.
- example of modular coding. The indicator logic is defined in the `signal_function`, and just by changing the implementation of this function, it is easy to create similar strategies using any trading signals (e.g. RSI, price actions, candlesticks etc.)

```python
'''
A classic moving average crossover strategy.

**Logic:**
1. Calculate two moving averages for a single stock: one fast, one slow.
2. When the fast MA crosses above the slow MA, go long (buy).
3. When the fast MA crosses below the slow MA, exit the position (sell).
4. Change the signal function to adapt to other indicator(s).
'''
import pandas as pd
from blueshift.types import *
from blueshift.api import symbol, order_target_percent, schedule_function, date_rules,time_rules
from blueshift.api import set_algo_parameters, set_slippage, set_commission
from blueshift.finance import commission, slippage

def initialize(context:AlgoContext):
    '''
    Called once at the start of the algorithm.
    '''
    # Define our asset instrument
    context.assets = [symbol('RELIANCE'), symbol('ITC')]

    # Define parameters for our moving averages
    context.params = {
        'fast_ma_window':20,         # 20 min for short window
        'slow_ma_window':50,        # 50 min for short window
        'signal_frequency':5        # check signal every 5 min
    }
    # call the API method set_algo_parameters to accept parameters passed externally
    set_algo_parameters()

    # set slippage and trading costs to 0
    set_slippage(slippage.NoSlippage())
    set_commission(commission.NoCommission())

    # Schedule a function to run our logic daily, 30 minutes after market open.
    schedule_function(
        rebalance,
        date_rules.everyday(),
        time_rules.market_open(minutes=context.params['signal_frequency'])
    )

def rebalance(context:AlgoContext, data:DataPortal):
    '''
    This function is called by the scheduler and contains the core trading template.
    '''
    # Get historical price data to calculate moving averages.
    # `history` returns a pandas DataFrame.
    price_history = data.history(context.assets, 'close', 
                                 context.params['slow_ma_window'] + 5, # Get a bit of extra data
                                 '1m'
                                 )

    # If we don't have enough data yet, do nothing.
    price_history = price_history.dropna()
    if len(price_history) < context.params['slow_ma_window']:
        return

    # equal weight positions with full capital invested
    weight = 1.0/len(context.assets)

    # --- Trading Logic ---
    for asset in context.assets:
        signal = signal_function(context, price_history[asset]) # type: ignore

        if signal==1:
            # Go long the target weight
            order_target_percent(asset, weight)
        else:
            # Go short the target weight
            order_target_percent(asset, -weight)


def signal_function(context:AlgoContext, px:pd.Series):
    ''' core logic of the signal calculation. Change it to implement different indicators/signals. '''
    # --- signal Logic ---
    # Calculate the fast and slow moving averages
    fast_ma = px.rolling(window=context.params['fast_ma_window']).mean()
    slow_ma = px.rolling(window=context.params['slow_ma_window']).mean()

    # Get the most recent values for the moving averages
    latest_fast_ma = fast_ma.iloc[-1]
    latest_slow_ma = slow_ma.iloc[-1]

    # return long signal if fast > slow, else short signal
    if latest_fast_ma > latest_slow_ma:
        # Crossover BUY signal: fast MA crosses above slow MA
        return 1
    else:
        # Crossover SELL signal: fast MA crosses below slow MA
        return -1

```

### 2.2 Example 2: Intraday Short Straddle

This is a complete, functional example of an options strategy. It demonstrates 

- the use of schedule functions to for flexible and responsive strategy logic.
- rolling options symbology, and convert them to dated instrument (with fixed expiry and strikes).
- how to set stoploss and take-profit targets. 
- basic error handling

```python
"""
An intraday short straddle strategy with stoploss and take-profits

**Logic:**
1. Sells a straddle (a call and a put at the ATM strike) in the morning at 09:30 AM
2. Set stoploss and take-profit targets at 40% of premiums.
3. If we hit stoploss or take-profit on one leg, the other continues
3. Square-off everything in the afternoon at 15:00 PM
"""
from blueshift.types import *
from blueshift.api import symbol, order, square_off, terminate
from blueshift.api import set_stoploss, set_takeprofit, get_datetime
from blueshift.api import schedule_function, date_rules, time_rules
from blueshift.api import set_slippage, create_order, set_commission, schedule_soon
from blueshift.finance.slippage import NoSlippage
from blueshift.finance.commission import NoCommission

def initialize(context: AlgoContext):
    ''' This function is called once at the start of the strategy. '''
    context.params = {
            'lots':1,
            'stoploss':0.4,
            'takeprofit':0.4,
            'start':'09:30',
            'end':'15:00',
            }
    
    set_slippage(NoSlippage(max_volume=0))
    set_commission(NoCommission())

    start = context.params['start']
    end = context.params['end']
    schedule_function(enter, date_rules.everyday(), time_rules.at(start))
    schedule_function(close_out, date_rules.everyday(), time_rules.at(end))

def enter(context:AlgoContext, data:DataPortal):
    dt = get_datetime()
    # options has format as "TICKER{Exp}{CE|PE}{STRIKE}, where Exp can be W0, or W1 for 
    # week 1, week 2 etc. For monthly expiries, it I or II etc for current and next month.
    # strike can be offset from ATM (e.g. +200 means 200 points from ATM).
    opts = [
        symbol('NIFTY-W0CE+0', dt=dt, use_spot=True),
        symbol('NIFTY-W0PE+0', dt=dt, use_spot=True),
    ]
    f = lambda context, data:place_entry_orders(opts, context, data)

    # schedule the function to run as soon as possible
    schedule_soon(f)

def place_entry_orders(opts:list[Asset], context:AlgoContext, data:DataPortal):
    lots = int(context.params['lots'])

    for asset in opts:
        qty = lots*asset.mult
        # pre-create the order object
        o = create_order(asset, -qty, validity='ioc')
        # place orders with automatic retries
        oid = order(o, None, max_retries=5)
        if not oid:
            handle_order_failure(context, asset)
        else:
            sl = float(context.params['stoploss'])
            tp = float(context.params['takeprofit'])
            set_stoploss(asset, method='percent', target=sl)
            set_takeprofit(asset, method='percent', target=tp)

def close_out(context:AlgoContext, data:DataPortal):
    # square off all positions and cancel any open orders
    square_off()

def handle_order_failure(context:AlgoContext, asset:Asset):
    # basic error handling, gracefully exit on error
    msg = f'failed to place order for asset {asset}'
    terminate(msg)
```

---

## 3. API Reference

Below are the key callback functions, objects and API functions available in the Blueshift API.

### 3.1. Core Event Callback Functions

These are specific functions that can be defined by the user and is automatically triggered by the Blueshift runtime based on specific events. They should be defined at the top level of the strategy code.

*   `initialize(context:AlgoContext) -> None`: Run once at the start of the algo. Used for initial algo setup and scheduling.

*   `on_data(context:AlgoContext, data:DataPortal) -> None`: Run on every tick of new price data.

*   `before_trading_start(context:AlgoContext, data:DataPortal) -> None`: Run on every tick of new price data.

---

### 3.2. Context Object (`context`)

The `context` object of type `AlgoContext` is passed to the core callbacks and scheduling functions and provides methods to access the state of the algo (e.g. positions, orders etc.). It is also used to store 
user defined variables to pass them around across different strategy functions.

*   `context.mode`: (Enum) The algo mode (`AlgoMode.LIVE`| `AlgoMode.BACKTEST`| `AlgoMode.PAPER`)
*   `context.state`: (dict) the current snapshot of the user defined state variables.
*   `context.timestamp`: (pandas.Timestamp) the last updated timestamp for the algo.
*   `context.trading_calendar`: (object) A `TradingCalendar` object representing the algo calendar.
*   `context.orders`: (dict) A dictionary of `Order` objects, keyed by order IDs for all orders placed by the algo.

The `context.portfolio` object provides information about the trading portfolio.

*   `context.portfolio.cash`: (float) The current cash balance.
*   `context.portfolio.starting_cash`: (float) The initial capital of the algo.
*   `context.portfolio.pnls`: (float) The current total profit and loss (booked + unrealized) of the algo.
*   `context.portfolio.mtm`: (float) The current unrealized profit and loss of the algo.
*   `context.portfolio.positions`: (dict) A dictionary of `Position` objects, keyed by asset.
*   `context.portfolio.portfolio_value`: (float) The total value of the portfolio (cash + positions).

The `context.account` object provides information about the trading account.

*   `context.account.gross_leverage`: (float) The current gross leverage.
*   `context.account.net_leverage`: (float) The current net leverage.
*   `context.account.gross_exposure`: (float) The current gross exposure.
*   `context.account.net_exposure`: (float) The current net exposure.

---

### 3.3. Data Object (`data`)

The `data` object is of type `DataPortal` and is passed to the core callbacks and scheduling functions and provides methods to access price data.

*   `data.current(assets:Asset, columns)`: Gets the most recent value for a given field.
    *   **Parameters:**
        *   `assets` (Asset or list of Assets): The security/securities to get data for.
        *   `columns` (str or list of str): The data field(s) to retrieve, e.g., 'price', 'open', 'high', 'low', 'close', 'volume'.
    *   **Returns:** A single value if one asset and field are requested, otherwise a pandas Series or DataFrame.

*   `data.history(assets, columns, nbars, frequency)`: Fetches a lookback window of historical data.
    *   **Parameters:**
        *   `assets` (Asset or list of Assets): The security/securities.
        *   `columns` (str or list of str): The data field(s).
        *   `nbars` (int): The number of bars (time steps) to retrieve.
        *   `frequency` (str): The resolution of the data, either '1d' for daily or '1m' for minutely.
    *   **Returns:** A pandas DataFrame with the requested historical data.

### 3.4. The `symbol` API Function and Asset Symbol Format

The `symbol` function must be imported from `blueshift.api`

*   `symbol(symbol_str)`: Resolves a string ticker into a `Asset` object.
    *   **Parameters:**
        *   `symbol_str` (str): The stock symbol, e.g., 'AAPL'.
        *   `dt` (pandas.Timestamp): The current timestamp to resolve a rolling futures or option instrument
        *   `use_spot` (bool): Use spot price (instead of futures price) to resolve a rolling instrument
    *   **Returns:** An `Asset` object.

The symbology followed by the `symbol` function is as below

- `symbol("NIFTY")` or `symbol("SPY")`: format is `symbol(TICKER)` for equities, indices or ETFs
- `symbol("EUR/USD")` or `symbol("BTC/USD")`: format is `QUOTE/BASE` for currencies and cryptos
- `symbol(NIFTY20251125FUT)`: NIFTY 25th Nov 2025 futures. Format is `TICKER{YYYYMMDD}FUT`
- `symbol(NIFTY20251125CE25000)`: NIFTY 25th Nov 2025 call strike 25000. Format is `TICKER{YYYYMMDD}CE{STRIKE}` for calls and `TICKER{YYYYMMDD}PE{STRIKE}` for puts.
- `symbol(NIFTY-I)`: NIFTY current month futures. Format is `TICKER-{Exp}` where `Exp` is `I` for first month, `II` for next etc.
- `symbol(NIFTY-ICE+0)`: NIFTY current month ATM call. Format is `TICKER-{Exp}CE{OFFSET}` for calls, and `TICKER-{Exp}PE{OFFSET}` for puts, where `OFFSET` is signed number of points away from ATM.
- `symbol(NIFTY-W0PE-200)`: NIFTY current week ATM-200 put. Format is `TICKER-{Exp}CE|PE{OFFSET}` where `Exp` is `W0` for current week, `W1` for next etc.
- `symbol(NIFTY-W0PE25D)`: NIFTY current week 25 Delta put. Format is `TICKER-{Exp}CE|PE{DELTA}D` where `DELTA` is Delta number multiplied by 100.
- `symbol(NIFTY-W0PE5000P)`: NIFTY current week put with price nearest to 50. Format is `TICKER-{Exp}CE|PE{PRICE}P` where `PRICE` is option price in cents.

---

### 3.5 Scheduling Functions and Rules

Scheduling functions allows finer control of trading logic flow. These must be imported from `blueshift.api`

*   `schedule_soon(func)`: Schedules a function to be run as soon as possible.
    *   **Parameters:** `func` (function): The function to call with signature `func(context, data)`.

*   `schedule_later(func, delay)`: Schedules a function to be run after a delay.
    *   **Parameters:**
        *   `func` (function): The function to call with signature `func(context, data)`.
        *   `delay`: (float): Number (or fraction) of minutes of delay

*   `schedule_function(func, date_rule, time_rule)`: Schedules a function to be called on a recurring basis.
    *   **Parameters:**
        *   `func` (function): The function to call with signature `func(context, data)`.
        *   `date_rule`: When to run the function (e.g., `date_rules.everyday()`, `date_rules.week_start()`).
        *   `time_rule`: What time to run the function (e.g., `time_rules.market_open(minutes=30)`).

Available `date_rules` and `time_rules` 

- `date_rules.everyday()`: run everyday. `date_rules.every_day()` is also acceptable.
- `date_rules.expiry(context, asset, offset=0)`: run `offset` days before the expiry day of the asset. The asset must be a futures or an option instrument.
- `date_rules.week_start(offset=0)` or `date_rules.month_start(offset)`: run `offset` days after week or month start
- `date_rules.week_end(offset=0)` or `date_rules.month_start(offset)`: run `offset` days before week or month end

- `time_rules.at("15:00")`: run at the specified time (string in HH:MM format or datetime.time) - in this case at 3:00 PM
- `time_rules.every_nth_minute(n=1)`: run at every n-th minute (int)
- `time_rules.market_open(minutes=0)`: run `minutes` minutes (int) after market opens
- `time_rules.market_close(minutes=0)`: run `minutes` minutes (int) before market opens

---

### 3.6 Order Functions

These functions are used to place and manage orders. These must be imported from `blueshift.api`

*   `create_order(asset, quantity, limit_price=0, validity='day')`: Create an `Order` object
    *   **Parameters:**
        *   `asset` (Asset): The asset to order.
        *   `quantity` (float): The order quantity (negative for sell)
        *   `limit_price` (float): Non-zero limit price makes it a limit order, otherwise market order
        *   `validity` (str): Use `ioc` for immediate-or-cancel, `day` otherwise for day validity
    *   **Returns:** The `Order` object

*   `order(asset, quantity, limit_price=0, validity='day')`: Places an order
    *   **Parameters:**
        *   `asset` (Asset): The asset to order.
        *   `quantity` (float): The order quantity (negative for sell)
        *   `limit_price` (float): Non-zero limit price makes it a limit order, otherwise market order
        *   `validity` (str): Use `ioc` for immediate-or-cancel, `day` otherwise for day validity
    *   **Returns:** (str): The order ID.

*   `order(asset, quantity, limit_price=0, validity='day')`: This is an overloaded signature to use  `Order` objects to place order
    *   **Parameters:**
        *   `asset` : A list of `Order` objects created by `create_order`
        *   `max_retries` (int): Number of retries to place the order
    *   **Returns:** (list): A list of order IDs.

*   `order_target(asset, quantity)`: Places an order for a specific number of shares.
    *   **Parameters:**
        *   `asset` (Asset): The security to order.
        *   `quantity` (int): The number of shares. A negative number is for shorting.
    *   **Returns:** (str): The order ID.

*   `order_target_value(asset, value)`: Places an order for a specific monetary value of an asset as target.
    *   **Parameters:**
        *   `asset` (Asset): The security to order.
        *   `value` (float): The amount in currency to order. A negative value indicates a short position.
    *   **Returns:** (str): The order ID.

*   `order_target_percent(asset, target)`: Places an order to adjust the asset's allocation to a target percentage of the portfolio value.
    *   **Parameters:**
        *   `asset` (Asset): The security to order.
        *   `target` (float): The target percentage (e.g., `1.0` for 100%, `0.5` for 50%, `0.0` to liquidate).
    *   **Returns:** (str): The order ID.

*   `cancel_order(order_id)`: Cancel an open order by order ID.
    *   **Parameters:** `order_id` (str) - The order ID to cancel.

*   `update_order(order_id, quantity)`: Modify the quantity an open order by order ID.
    *   **Parameters:**
        *   `order_id` (str) - The order ID to modify.
        *   `quantity` (int): The new quantity for the order.

*   `square_off(assets=None)`: square-off existing positions.
    *   **Parameters:** `assets` (list) - A list of `Asset`. If `None` square-off all existing positions.
    *   **Returns:** (bool): True if success.

*   `get_open_orders()`: Retrieves a dictionary of `Order` objects, keyed by order IDs for all open orders.

*   `schedule_order_callback(order_ids, on_order_complete, timeout=1, on_timeout)`: Pass a list of order IDs and a callback to invoke once none of the orders are open anymore.
    *   **Parameters:**
        *   `order_ids` (list) - A list of order ID to watch.
        *   `on_order_complete` (function): The callback on completion, signature is `func(context, order_ids)`
        *   `timeout` (float): Number of minutes (or fraction) to wait for.
        *   `on_timeout` (function): Callback on timeout, signature is `func(context, order_ids)`

*   `wait_for_trade(order_ids, timeout=1)`: Pass a list of order IDs and wait for their execution or till times out. This will block the algo flow.
    *   **Parameters:**
        *   `order_ids` (list) - A list of order ID to watch.
        *   `timeout` (float): Number of minutes (or fraction) to wait for.

---

### 3.7. Stoploss and Risk Management APIs

Import these functions from `blueshift.api` before use.

*   `set_stoploss(asset, method, target, trailing=False, on_stoploss=None, skip_exit=False)`: Set a position wise or strategy wise stoploss target
    *   **Parameters:**
        *   `asset` (Asset or None) - Asset for the stoploss, or `None` for strategy level stoploss
        *   `method` (str): `percent` or `move` or `price` for percent, relative or absolute price targets. For strategy level, specify either `amount` or `pnl` for unrealized or total loss targets
        *   `trailing` (bool): Enable trailing stoploss.
        *   `on_stoploss` (function): Callback on stoploss trigger, signature is `func(context, asset)`
        *   `skip_exit` (bool): Skip the position exit, just trigger the `on_stoploss` callback

*   `set_takeprofit(asset, method, target, on_takeproft=None, skip_exit=False)`: Set a position wise or strategy wise take-profit target
    *   **Parameters:**
        *   `asset` (Asset or None) - Asset for the take-profit, or `None` for strategy level stoploss
        *   `method` (str): `percent` or `move` or `price` for percent, relative or absolute price targets. For strategy level, specify either `amount` or `pnl` for unrealized or total profit targets
        *   `on_takeproft` (function): Callback on take-profit trigger, signature is `func(context, asset)`
        *   `skip_exit` (bool): Skip the position exit, just trigger the `on_takeproft` callback

*   `set_exit_policy(cancel_orders=True, square_off=False)`: Set auto square-off policy for the algo on exit. Can be called only inside `initialize`.
    *   **Parameters:**
        *   `cancel_orders` (bool) - cancel all open orders if True
        *   `square_off` (bool): cancel all open orders and square-off all positions if True

*   `set_cooloff_period(period=30)`: square-offs automatically trigger a cool-off period during which further square-off or entry is prohibited. Set the period for this cool-off. Can be called only inside `initialize`.
    *   **Parameters:** `period` (float) - Number of minutes or fractions.

*   `terminate(error)`: Terminate the algo run immediately, with an error message
    *   **Parameters:** `error` (str) - An error message - reason to terminate.

*   `finish(msg)`: End the algo run gracefully, with an exit message.
    *   **Parameters:** `msg` (str) - An exit message - final status message.

---

### 3.8. Asset, Order and Position Objects

`Asset` object represents a tradable instrument, like equities, futures, options etc

*   `asset.symbol`: (str) the asset ticker
*   `asset.name`: (str) the full name of the instrument
*   `asset.exchange_name`: (str) the exchange name where traded
*   `asset.mult`: (float) the lot size of the instrument
*   `asset.is_futures()`: True if it is a futures instrument
*   `asset.is_opt()`: True if it is an option instrument
*   `asset.is_rolling`: (str) True if it is a rolling futures or options instrument

`Order` object represent an order - along with details like fill, status etc.

*   `order.asset`: (Asset) the asset for the order
*   `order.oid`: (str) the order ID
*   `order.quantity`: (float) the ordered quantity without sign
*   `order.filled`: (float) the already filled amount
*   `order.price`: (float) the limit price of the order if non-zero, else a market order
*   `order.is_buy`: True if the order is a buy order, False for a sell order
*   `order.is_open`: True if the order is open
*   `order.is_done`: True if the order is fully completed
*   `order.is_cancelled`: True if the order is fully or partially cancelled
*   `order.is_final`: True if the order is not open anymore

`Position` object represent a position - along with details like side, open quantity etc.

*   `position.asset`: (Asset) the asset for the position
*   `position.quantity`: (float) the open quantity with sign (long position for positive, short for negative)
*   `position.unrealized_pnl`: (float) the unrealized profit or loss
*   `position.pnl`: (float) total profit or loss - booked + unrealized
*   `position.value`: (float) the exposure value of the position
*   `position.cost_basis`: (float) the cost basis of the position

---

### 3.9. Slippage and Cost Simulation APIs

Import these functions from `blueshift.api` before use. Skip them to use default models.

*   `set_slippage(model)`: Select the slippage model
    *   **Parameters:** `model` (SlippageModel) - A `SlippageModel` to use for backtest slippage cost simulation.

*   `set_commission(model)`: Select the slippage model
    *   **Parameters:** `model` (CostModel) - A `CostModel` to use for backtest trading cost simulation.

*   `set_margin(model)`: Select the slippage model
    *   **Parameters:** `model` (MarginModel) - A `MarginModel` to use for backtest margin simulation.

The available slippage, cost and margin models are below. They must be imported from `blueshift.finance.slippage`, `blueshift.finance.commission` and `blueshift.finance.margin` respectively

*   `NoSlippage(max_volume=0.02)`: A zero slippage model, specify `max_volume` to define the volume participation, or set to 0 for fill for any quantity

*   `NoCommission()`: Zero trading cost

*   `FlatMargin(intial_margin=0.10, maintenance_margin=None)`: Flat percentage margin model. Specify `initial_margin` for new orders, and `maintenance_margin` for a different value maintenance margin on overnight positions.

---

### 3.10. Algo State Management

Most regular state (like open positions, orders, profit and loss) etc are automatically tracked by the `context` variable. If custom state management is needed, the recommended way is to create a dictionary `context.algo_state` and store your state variables as keys there. Use `record_state("algo_state")` to automatically persist the states on algo exit. Use `load_state()` to load any saved state from previous runs. Both functions can be imported from `blueshift.api`.

**important**: the `context.algo_state` can only capture builtin variables types like strings, boolean values, numbers and builtin containers like lists, sets or dictionaries. Special objects or user created types are not allowed. It must be JSON serializable.

---

## 4. Whitelisted Python packages

The core `blueshift` package and the following well-known Python packages are whitelisted and can be used. No other packages must be used for developing trading strategies.

- **blueshift**: the Blueshift engine package.
- **bisect**: an useful array sorting package.
- **collections**: advanced containers
- **cvxopt**: package for convex optimization.
- **cvxpy**: a “nice and disciplined” interface to cvxopt.
- **datetime**: for manipulating dates and times in both simple and complex ways.
- **functools**: higher-order functions and operations on callable objects.
- **hmmlearn**: for unsupervised learning and inference of Hidden Markov Models.
- **hurst**: for analysing random walks and evaluating the Hurst exponent.
- **arch**: ARCH and other tools for financial econometrics.
- **math**: provides access to the mathematical functions defined by the C standard.
- **numpy**: package for scientific computing with Python.
- **pandas**: high-performance, easy-to-use data structures and data analysis tools.
- **pykalman**: implements Kalman filter and Kalman smoother in Python.
- **random**: random number generators for various distributions.
- **scipy**: efficient numerical routines for scientific computing.
- **sklearn**: for machine learning in Python.
- **statsmodels**: for statistics in Python.
- **talib**: for technical analysis in Python.
- **xgboost**: xgboost implementation for Python.

---

## 5. Best Practices

*   Check for sufficient and valid (not NaN) data when using `data.history` or `data.current`.
*   Use `get_datetime()` imported from `blueshift.api` to query the current timestamp - this works for both backtesting and live trading.
*   Use `set_exit_policy(square_off=True)` for intraday algos to ensure auto square-off on exit, even with unhandled errors. This can only be called inside `initialize`.
*   Do not use underscore (`_`) as the leading or trailing character of a variable function name
*   Do not use `schedule_later` in the `initialize` or `before_trading_start`.
*   Use `schedule_funtion` only inside `initialize` and not anywhere else.
*   Order placement does not wait for the order execution. Use `wait_for_trade` to wait for execution, or use `schedule_order_callback` to get notified and invoke your callback on execution.
*   Stoplosses or take-profits reset daily or on restart. Use `before_trading_start` to re-instate them for overnight positions.
*   Always use the `dt` argument** in the `symbol` function to place order with a rolling asset symbol.
*   Prefer to catch `OrderAlreadyProcessed` error for order cancel and update, as the order may already have been filled. Import it from `blueshift.errors`.
*   Prefer to catch `SymbolNotFound` error in calls to `symbol` function. Import it from `blueshift.errors`.
*   Prefer to catch `OrderError` while placing orders. Import it from `blueshift.errors`.
*   Do not just check `context.portfolio.positions` to see we have already traded. The order placed already may be still open and has not created a position yet. Check for any open orders as well.
*   Use proper error handling whenever applicable
*   If required, parameterize your strategy using `set_algo_parameters()` imported from `blueshift.api` and use `context.params` dictionary to manage.
*   Keep your strategy logic modular and functions small and quick for best results.