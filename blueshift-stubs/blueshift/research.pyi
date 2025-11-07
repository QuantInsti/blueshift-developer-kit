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
import pandas
from .assets import Asset
from .pipeline import Pipeline

def list_datasets(name:str) -> None:
    """ list available datasets. """
    ...

def use_dataset(name:str) -> None:
    """ select and set the specified dataset for future queries. """
    ...

def symbol(sym:str, dt:pandas.Timestamp, *args, **kwargs) -> Asset:
    """ convert ticker to asset object. """
    ...

def sid(sec_id:int) -> Asset:
    """ convert security ID to asset object. """
    ...

def current(asset:Asset|list[Asset], columns:str|list[str]) -> float|pandas.Series|pandas.DataFrame:
        """fetch latest price data from selected dataset. """
        ...

def history(asset:Asset|list[Asset], columns:str|list[str], nbars:int, frequency:str) -> pandas.Series| pandas.DataFrame:
        """fetch historical price data from selected dataset. """
        ...

def fundamentals(asset:Asset|list[Asset], metrics:str|list[str], nbars:int, frequency:str) -> pandas.Series| pandas.DataFrame:
        """fetch corporate fundamental data from selected dataset. """
        ...

def list_sectors(frequency:Literal['Q','A']) -> list[str]:
      """list available sectors for the given frequency - quarterly (Q) or annual(A). """
      ...

def get_sectors(frequency:Literal['Q','A']) -> pandas.DataFrame:
      """list available sectors for the given frequency - quarterly (Q) or annual(A). """
      ...

def run_pipeline(pipeline:Pipeline, start_date:pandas.Timestamp, end_date:pandas.Timestamp) -> pandas.DataFrame:
      """run and get the output of a pipeline object between the dates. """
      ...