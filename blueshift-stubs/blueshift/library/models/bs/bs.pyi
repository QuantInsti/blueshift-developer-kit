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
import numpy
import pandas
from blueshift.types import AlgoContext

def bs_plain_vanilla_option(atmf:float, strike:float, imp_vol:float, time:float|pandas.Timedelta, 
                            option_type:Literal["CALL","PUT"], 
                            annualization_factor:float=252,
                            context:AlgoContext|None=None) -> float:
    """ calculate Black Scholes option prices. """
    ...

def bs_plain_vanilla_optionv(atmf:numpy.ndarray, strike:numpy.ndarray, imp_vol:numpy.ndarray, 
                             time:numpy.ndarray|list[str]|list[pandas.Timedelta], 
                             option_type:Literal["CALL","PUT"], annualization_factor:float=252, 
                             context:AlgoContext|None=None) -> numpy.ndarray:
    """ vectorized version of Black Scholes option price function. """
    ...

def bs_implied_vol(atmf:float, strike:float, price:float, time:float|pandas.Timedelta, 
                            option_type:Literal["CALL","PUT"], 
                            annualization_factor:float=252,
                            context:AlgoContext|None=None) -> float:
    """ get Black-Scholes implied vol from price. """
    ...

def bs_implied_volv(atmf:numpy.ndarray, strike:numpy.ndarray, price:numpy.ndarray, 
                             time:numpy.ndarray|list[str]|list[pandas.Timedelta], 
                             option_type:Literal["CALL","PUT"], annualization_factor:float=252, 
                             context:AlgoContext|None=None) -> numpy.ndarray:
    """ vectorized version of Black Scholes implied vol function. """
    ...

def bs_plain_vanilla_greek(atmf:float, strike:float, imp_vol:float, time:float|pandas.Timedelta, 
                           option_type:Literal["CALL","PUT"], 
                           greek:Literal['DELTA', 'VEGA','THETA', 'GAMMA'], 
                           annualization_factor:float=252,
                           context:AlgoContext|None=None) -> float:
    """ get Black-Scholes option greeks. """
    ...

def bs_plain_vanilla_greekv(atmf:numpy.ndarray, strike:numpy.ndarray, imp_vol:numpy.ndarray, 
                            time:numpy.ndarray|list[str]|list[pandas.Timedelta], 
                           option_type:Literal["CALL","PUT"], 
                           greek:Literal['DELTA', 'VEGA','THETA', 'GAMMA'], 
                           annualization_factor:float=252,
                           context:AlgoContext|None=None) -> float:
    """ vectorized version of Black Scholes option greeks function. """
    ...