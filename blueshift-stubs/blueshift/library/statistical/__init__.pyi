# Copyright 2024 QuantInsti Quantitative Learnings Pvt Ltd.
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
from typing import Tuple, Literal
import pandas
import numpy

from blueshift.library.common import Line

def find_imp_points(x:pandas.Series|pandas.DataFrame, R:float|None=None, scale:float=2.5, 
                    inclusive:bool=True) -> Tuple[pandas.Index, pandas.Index, pandas.Series|pandas.DataFrame]:
    """ find perceptually important points. """
    ...

def find_trends(x:pandas.Series|pandas.DataFrame, type_:Literal['price','variance']='price', 
                Q:int=10, minseglen:int=10, penalty:float=2) -> list[Line]:
    """ find change point in price levels or variance. """
    ...

def get_hmm_state(x:pandas.Series, covariance_type:str='full', n_iter:int=100) -> pandas.Series:
    """ classification based on hidden market model. """
    ...

def hedge_ratio(Y:pandas.Series|numpy.ndarray, X:pandas.Series|numpy.ndarray) -> Tuple[float, float]:
    """ returns the ADF p-value and regression coefficient. """
    ...

def z_score(Y:pandas.Series|numpy.ndarray, X:pandas.Series|numpy.ndarray|None=None, 
            lookback:int|None=None, coeff:float|None=None) -> float:
    """ computes the z-score of `Y` or residual of `Y` regressed on `X`. """
    ...