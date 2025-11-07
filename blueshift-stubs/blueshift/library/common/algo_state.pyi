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
from blueshift.types import AlgoContext, DataPortal

class AlgoStateMachine:
    def __init__(self, states:list[str], transitions:dict[str,list[str]], 
                 on_state_change:Callable[[AlgoContext,str,str],None]|None=None, 
                 initial_state:str|None=None, 
                 error_handler:Callable[[AlgoContext,str,str],None]|None=None):
        """A simple state machine for maintaining states of complex algos. """
        ...

    @property
    def state(self):
        """current state. """
        ...

    @state.setter
    def state(self, value):
        """ setter for state. """
        ...

    def initialize(self, context:AlgoContext) -> None:
        """ initialize the state machine. """
        ...

    def add_transitions(self, transitions:dict[str,list[str]]) -> None:
        """ overwrite the initial transitions. """
        ...

    def trigger_event(self, state:str, check_before:bool=False, 
                      ignore_error:bool=False) -> Callable[[AlgoContext,DataPortal],None]:
        """ returns a blueshift callback that triggers transition from current to target `state`"""
        ...

    def can_transition_to(self, state:str) -> bool:
        """check if transition to a target `state` is valid. """
        ...

    def transition_to(self, state:str, ignore_error:bool=False) -> None:
        """ trigger transition to a target `state`. """
        ...

    def ensure_state(self, states:str|list[str], err_msg:str="", 
                     ignore_error:bool=False) -> Callable:
        """ a useful decorator for strategy functions to ensure a given state. """
        ...