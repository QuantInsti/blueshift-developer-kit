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
from typing import Callable, Any
from blueshift.lib.common.sentinels import NotSpecified, Sentinel

from ..term import ComputableTerm
from ..filters import Filter
from ..factors import Factor

class Classifier(ComputableTerm):
    """ pipline classifier. """
    def eq(self, other:ComputableTerm) -> Filter:
        """ create a filter when asset/date pair value is equal. """
        ...

    def __ne__(self, other:Any) -> Filter:... # type: ignore[override]

    def startswith(self, prefix:str) -> Filter:...
    def endswith(self, prefix:str) -> Filter:...
    def has_substring(self, substring:str) -> Filter:...
    def matches(self, pattern:str) -> Filter:...
    def relabel(self, relabeler:Callable[[str],str]) -> Classifier:...
    def element_of(self, choices:list[str]|list[int]) -> Filter:...
    def peer_count(self, mask:Filter|Sentinel=NotSpecified) -> Factor:...

class CustomClassifier(Classifier):
    """ custom classifier. """

class Latest(CustomClassifier):
    """ latest value. """
    
__all__ = [
    'Classifier',
    'CustomClassifier',
    'Latest',
]