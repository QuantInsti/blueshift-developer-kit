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
from typing import Literal, Any

class Term:
    """ pipeline term. """
    ...

class LoadableTerm(Term):
    """ pipeline loadable term. """
    ...

class ComputableTerm(Term):
    """ pipeline computable term. """
    def downsample(self, 
                   frequency:Literal['year_start', 'quarter_start', 'month_start', 'week_start']) -> ComputableTerm:
        """ downsample a term. """
        ...

    def alias(self, name:str) -> ComputableTerm:
        """ name alias for this term. """
        ...

    def isnull(self) -> ComputableTerm:
        """ A filter with True for missing data in this term. """
        ...

    def notnull(self) -> ComputableTerm:
        """ A filter with False for missing data in this term. """
        ...

    def fillna(self, fill_value:Any) -> ComputableTerm:
        """ return a new term with filled NA values. """
        ...