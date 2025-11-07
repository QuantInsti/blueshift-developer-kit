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

from .factors import CustomFactor
from .filters import CustomFilter, Filter
from .classifiers import CustomClassifier, Classifier
from .factors import Factor, CustomFactor
from .term import ComputableTerm, Term, LoadableTerm

class Pipeline:
    """ Pipeline class. """
    columns:dict[str, ComputableTerm]
    screen:Filter|None

    def add(self, term:ComputableTerm, name:str, overwrite:bool=False):
        """ add a factor as column. """
        ...

    def remove(self, name:str):
        """ remove the column. """
        ...

    def set_screen(self, screen:Filter, overwrite:bool=False):
        """ add a filter. """
        ...

__all__ = (
    'Classifier',
    'CustomFactor',
    'CustomFilter',
    'CustomClassifier',
    'Classifier',
    'Factor',
    'Filter',
    'LoadableTerm',
    'ComputableTerm',
    'Pipeline',
    'Term',
)