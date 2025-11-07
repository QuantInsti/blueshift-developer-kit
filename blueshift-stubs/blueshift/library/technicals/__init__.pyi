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

from typing import Literal, Callable, Tuple
import pandas
import numpy

from blueshift.library.common import Line, Pattern

class PatternDef:
    name:str
    desc:str
    size:int

    def __init__(self, name:str, desc:str, 
                 func:Callable[[numpy.ndarray,list[Line],float,bool],Tuple[bool, float, float]], 
                 size:int, tolerance:float|None=None):
        """ 
            pattern definition with a search function `func` that takes  array of 
            data points of size `size`, and returns a tuple. The first value of 
            the tuple is true if pattern is found. The next is the level for breach, 
            and last is a shape metric (aspect).
        """
        ...

    def match(self, points:numpy.ndarray, trends:list[Line]|None=None, 
              data:pandas.Series|numpy.ndarray|None=None, tolerance:float|None=None, 
              adjust_trend=False) -> Tuple[bool, float, float]:
        """ run a match. """
        ...

def find_support_resistance(x:pandas.Series|pandas.DataFrame, type_:Literal['pip','fibonacci']='pip', 
                            R:float|None=None, scale:float|list[float]=[1.75, 2, 2.5, 3, 5, 7], 
                            tolerance:float=0.001) -> list[Line]:
    """ find support(s) and Resistance(s) lines. """
    ...

def search_chart_patterns(data:pandas.Series|pandas.DataFrame, pattern:str|PatternDef, 
                          R:float|list[float]|None=None, 
                          scale:float|list[float]=[1.75, 2, 2.5, 3, 5, 7], 
                          tolerance:float|None=None, find_all:bool=False, 
                          adjust_trend:bool=False) -> list[Pattern]:
    """ find chart patterns in input data. """
    ...