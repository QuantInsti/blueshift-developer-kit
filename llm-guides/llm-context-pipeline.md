---
title: Blueshift LLM Pipeline Strategy Developer Guide
version: 1.0
framework: blueshift
purpose: |
  This guide enables large language models (e.g., ChatGPT) to generate accurate Python strategy code 
  using the Blueshift Pipeline API for screening and ranking a large universe of assets.

usage_instructions:
  - Import the type definition module for code autocomplete: `from blueshift.types import *` at the start of the strategy code. It is not an error if not used, but a recommendation.
  - Always import necessary modules from `blueshift.api`, `blueshift.pipelines` and other modules as specified.
  - Every strategy must define `initialize(context:AlgoContext)` function.
  - Always define `Pipeline` object and use it in the `attach_pipeline` API method.
  - Use `attach_pipeline` in the `initialize` function to add the pipeline to the algorithm.
  - Use `pipeline_output` in a scheduled function or in before_trading_start to get the results of the pipeline computation.
  - Make sure the `pipeline_output` is called once a day or at a lower frequency.
  - Eemember the pipelines are always evaluated on data at day frequency or lower.
  - Use only the whitelisted Python packages if required, do not use unsupported packages or libraries.
  - Use `print` or `log_info` sparingly. If really required, prefer `log_info` over `print`.
  - Generate concise and readable code.
  - Follow the structure and coding style in this document.

expected_behavior:
  - When the user describes a screening or ranking logic, generate a strategy that uses the Pipeline API.
  - The `rebalance` function (or a similarly scheduled function) should use the output of the pipeline to make trading decisions.
  - Always ensure code compiles and uses correct API calls.

example_usage_prompt: |
  "Using the uploaded Blueshift LLM Pipeline Strategy Developer Guide, write a strategy that goes long on the top 10 stocks with the highest 1-month momentum and short on the bottom 10 stocks with the lowest 1-month momentum, rebalancing weekly."

last_updated: 2025-11-05
compatible_blueshift_version: ">=5.0.0"
---

# Blueshift Pipeline Strategy Developer Guide (LLM Context)

## Table of Contents

- [1. Overview & Core Concepts](#1-overview--core-concepts)
  - [Key Components of a Pipeline Strategy](#key-components-of-a-pipeline-strategy)
- [2. Strategy Code Example](#2-strategy-code-example)
  - [2.1 Example: Momentum Factor Strategy](#21-example-momentum-factor-strategy)
- [3. API Reference](#3-api-reference)
  - [3.1. Core Pipeline Functions](#31-core-pipeline-functions)
  - [3.2. The `Pipeline` Object](#32-the-pipeline-object)
  - [3.3. Factors](#33-factors)
  - [3.4. Filters](#34-filters)
  - [3.5. Custom Factors and Filters](#35-custom-factors-and-filters)
- [4. Whitelisted Python packages](#4-whitelisted-python-packages)
- [5. Best Practices](#5-best-practices)

---

## 1. Overview & Core Concepts

The Blueshift Pipeline API is designed for building strategies that involve screening, ranking, and filtering a large universe of assets based on various quantitative factors. It provides an efficient way to compute values for each asset in a universe and select a subset for trading.

The Pipeline API is event-driven, similar to the core Blueshift API. You define a `Pipeline` that specifies the computations, attach it to your algorithm, and then access the results when your scheduled logic runs. Pipeline resuts are evaluated at a data frequency of daily or lower.

### Key Components of a Pipeline Strategy:

*   **`Pipeline` object:** The `Pipeline` object holds the definition of computation and filtering.
*   **Factor:** A computation that produces a numerical value for each asset (e.g., moving average, momentum, RSI).
*   **Filter:** A computation that produces a boolean value for each asset, used to include or exclude assets from the final output (e.g., assets with returns > 0 or RSI < 70>).
*   **`attach_pipeline` API function:** Connects the defined `Pipeline` to the algorithm.
*   **`pipeline_output` API function:** Lazily evaluate the results of the pipeline and return the results as a pandas DataFrame.

---

## 2. Strategy Code Example

### 2.1. Example: Momentum Factor Strategy

This example implements a long-only momentum strategy. It identifies the top performing stocks from a universe based on their 3-month (3*21 days) returns and takes long only positions accordingly.

```python
"""
A long-only time-series momentum strategy.

**Logic:**
1. Filter the universe based on liquidity and low beta 
2. Pick the stocks with top returns in recent months and go long
3. Go long with the chosen stocks, exiting anything else in the portfolio
4. Rebalance with the above logic every month
"""
from blueshift.library.pipelines import asset_beta
from blueshift.pipeline import Pipeline

from blueshift.pipeline.factors.statistical import vectorized_beta
from blueshift.pipeline import CustomFactor, CustomFilter
from blueshift.pipeline.data import EquityPricing
from blueshift.finance.slippage import NoSlippage
from blueshift.finance.commission import NoCommission

import talib as ta
import numpy as np
import warnings

from blueshift.errors import NoFurtherDataError
from blueshift.api import order_target_percent, schedule_function, log_info
from blueshift.api import symbol, date_rules, time_rules, get_datetime
from blueshift.api import attach_pipeline, pipeline_output
from blueshift.api import set_commission, set_slippage

def average_volume_filter(lookback, amount, context=None):
    ''' An example of custom filter wrapped in function. We use the closure to handle extra parameters.'''
    class AvgDailyDollarVolumeTraded(CustomFilter):
        inputs = [EquityPricing.close, EquityPricing.volume]
        def compute(self,today,assets,out,close,volume): # type: ignore[override]
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=RuntimeWarning)
                dollar_volume = np.nanmean(close * volume, axis=0)
            high_volume = dollar_volume > amount
            out[:] = high_volume
    
    return AvgDailyDollarVolumeTraded(window_length = lookback) # type: ignore[override]

class ROCFactor(CustomFactor):
    ''' An example of custom factor. We specify the window length while instantiating. '''
    inputs = [EquityPricing.close]
    def compute(self,today,assets,out,close): # type: ignore[override]
        out[:] = np.apply_along_axis(lambda col:ta.ROC(col, 63)[-1], axis=0, arr=close) # type: ignore[type]

def initialize(context):
    # set 0 costs
    set_slippage(NoSlippage(max_volume=0))
    set_commission(NoCommission())
    # The context variables can be accessed by other methods
    context.params = {'lookback':3, # months, multiply by 21 for business days.
                      'size':5, # max number of stocks in positions
                      'min_volume':1E7, # 10 million average traded volume threshold
                      'cash':0.2, # cash holding percentage
                      }
    
    # Call rebalance function on the first trading day of each month
    schedule_function(run_strategy, date_rules.month_start(), 
            time_rules.market_close(minutes=30))

    # Set up the pipe-lines for strategies
    attach_pipeline(make_screener(context), name='my_screener')

def make_screener(context):
    ''' an user defined function where we create the pipeline. '''
    pipe = Pipeline()

    # get the strategy parameters
    lookback = context.params['lookback']*21
    v = context.params['min_volume']

    # Set the volume filter using a custom filter with parameter passing
    volume_filter = average_volume_filter(lookback, v)
    # add a beta filter, using a built-in factors
    market = symbol('NIFTY')
    beta = asset_beta(market, 60, context)
    
    # compute past returns - using a custom factor directly
    roc_factor = ROCFactor(window_length=lookback+5) # type: ignore[override]
    
    pipe.add(roc_factor,'roc')
    pipe.add(beta,'beta')
    
    # comparing factors with numbers returns filters
    # we can also use math operators like '+', '-', '*' and '/' to combine factors or a factor and a number
    roc_filter = roc_factor > 0 # positive momentum only
    beta_filter = (beta > -0.5) & (beta < 0.5) # select a low beta filter
    
    # add the filtering
    pipe.set_screen(roc_filter & volume_filter & beta_filter) # combine filters with '&' or '|' operator

    return pipe

def screener(context, data):
    # get the pipeline output and select the top N
    try:
        pipeline_results = pipeline_output('my_screener')
    except NoFurtherDataError:
        log_info('no pipeline for {}'.format(get_datetime()))
        return []

    pipeline_results = pipeline_results.dropna() # remove NAs
    selected = pipeline_results.sort_values(
        'roc')[-(context.params['size']):] # pick up best N stocks
    
    # return the asset list, note the pipeline result dataframe has 
    # assets (that survived the filters) as index and the computed 
    # factors as the columns
    return selected.index.tolist()

def run_strategy(context, data):
    ''' scheduled to run on first business day of evevry month. '''
    # get screened assets to buy
    assets = screener(context, data)
    current_holdings = context.portfolio.positions.keys() # current holdings

    exits = set(current_holdings) - set(assets) # assets to sell
    for asset in exits:
        # exit the exiting assets
        order_target_percent(asset, 0)

    if assets:
        # rebalance the new list with equal weights
        sizing = (1-context.params['cash'])/len(assets)
        for asset in assets:
            order_target_percent(asset, sizing)
    
```

---

## 3. API Reference

### 3.1. Core Pipeline Functions

These functions, imported from `blueshift.api`, are the primary interface for using Pipelines.

*   `attach_pipeline(pipeline, name)`: Attaches a `Pipeline` object to the algorithm.
    *   **Parameters:**
        *   `pipeline` (`Pipeline`): The pipeline object.
        *   `name` (str): A name for this pipeline.

*   `pipeline_output(name)`: Retrieves the computed output of an attached pipeline.
    *   **Parameters:**
        *   `name` (str): The name given to the pipeline in `attach_pipeline`.
    *   **Returns:** A pandas DataFrame where the index is `Asset` objects that has passed the `Filter`s and columns are the added `Factor`s in the associated `Pipeline` object.

### 3.2. The `Pipeline` Object

This is the main object, imported from `blueshift.pipelines`.

*   `Pipeline(columns={}, screen=None)`: Constructor for a new pipeline.
    *   **Parameters:**
        *   `columns` (dict): A dictionary mapping column names (str) to `Factor`
        *   `screen` (`Filter`): A filter that defines the initial universe of assets for the pipeline computation. This is a performance optimization.
*   `add(term, name)`: Method to a factor to the pipeline object.
    *   **Parameters:**
        *   `term` (`Factor`): A factor to add to the pipeline object.
        *   `name` (str): The name of the factor, that will be the corresponding column name for the output.
*   `set_screen(screen)`: Method to set the filter to use with the pipeline object.
    *   **Parameters:**
        *   `screen` (`Filter`): A factor to add to the pipeline object. Combine multiple filters using the "&" (and) or the "|" (or) operator.

### 3.3. Factors

Factors produce numerical outputs. Import built-in factors from `blueshift.pipelines.factors`. You can also create custom factors by subclassing `CustomFactor`.

*   `Returns(window_length)`: Calculates the percentage change in price over a lookback window.
*   `SimpleMovingAverage(inputs, window_length)`: Calculates the simple moving average of a given input (usually `EquityPricing.close`).
*   `AverageDollarVolume(window_length)`: A factor that computes average traded volume.
*   And many more like `RSI`, `BollingerBands`, `RollingLinearRegression`, etc.

### 3.4. Filters

Filters produce boolean outputs and are used for screening. Import from `blueshift.pipelines.filters`. Create custom filters by subclassing `CustomFilter`.

*   `Top(inputs, count)`: A filter that selects the top `count` assets based on an input factor.
*   `Bottom(inputs, count)`: A filter that selects the bottom `count` assets.
*   And many more like `PercentileFilter`, `All`, `Any`, etc.

### 3.5. Custom Factors and Filters

Apart from the built-in factors and filters, you can define your custom factors and filters. 

To use custom factor, we need to define a new class, derived from `CustomFactor` class, implement the `compute` method of the class and set the `inputs`(a list - see below) and `window_length` (int) values either as class variable or during instantiation. The example at para 2.1 in this document defines a custom factor `ROCFactor`. Another example is show below:

```python
from blueshift.pipeline import Pipeline, CustomFilter, CustomFactor
from blueshift.pipeline.data import EquityPricing

class CloseAboveHighFactor(CustomFilter):
    inputs = [EquityPricing.close, EquityPricing.high]
    def compute(self,today,assets,out,close_price, high_price):
        out[:] = (close_price[-1] - high_price[-2])

```
Here we import the `inputs` columns from the required dataset (`EquityPricing` for OHLCV columns or `QuarterlyFundamental`/ `AnnualFundamental` for fundamental data). The compute function has the following signature

*   `compute(today, assets, out, *args)`: Add a factor to the pipeline object.
    *   **Parameters:**
        *   `today` (`Timestamp`): The date of computation.
        *   `assets` (ndarray): A numpy 1-D array of length N for all assets active that day.
        *   `out` (ndarray): A numpy 1-D array of shape N passed to the function that holds the return values.

    as positional arguments, the function also receives a TxN ndarray for each term defined in the `inputs` list, where `T` is the size of the `window_length`.

Defining a custom filter is very similar. The only differences are 1. we need to derive from the `CustomFilter` class instead of `CustomFactor` and 2. in the `compute` method, we should assign boolean values to `out` array instead of numbers. The example at 2.1 defines a custom filter `AvgDailyDollarVolumeTraded`.

---

## 4. Whitelisted Python packages

The same packages as in the core developer guide are available. See the main guide for the full list.

---

## 5. Best Practices

*   **Use `screen`:** Always use the `screen` parameter in the `Pipeline` constructor, or call `set_screen` later, to limit the initial universe of assets. This significantly improves performance.
*   **Combine Filters:** Use boolean operators (`&` for AND, `|` for OR) to combine multiple filters into a single, more complex filter.
*   **Combine Factors:** Use math operators (`+`,`-`,`*`,`/`) to combine multiple factors - or a factor and a number - into a single, more complex factor.
*   **Filter from Factor:** Use logical operators (`>`,`<`) to comapre a factor with a number - or another factor - to create a filter.
*   **Daily frequency:** Pipelines are evaluated at daily or lower data frequency. Calling them more than once per day is wasteful.
*   **Debugging:** To debug a pipeline, you can add intermediate factors as columns. Then, inspect the DataFrame returned by `pipeline_output` to understand the output of each step.
*   **Avoid Lookahead Bias:** Ensure that all data used in your pipeline factors is available at the time of computation. The Pipeline API is designed to help prevent this, but it's good practice to be mindful.
