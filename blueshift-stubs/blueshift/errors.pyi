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

class BlueshiftException(Exception):
    """ Blueshift error type. """
    ...

class ValidationError(BlueshiftException):
    """ input validation error. """
    ...

class SymbolNotFound(BlueshiftException):
    """ asset symbol not found. """
    ...

class ServerError(BlueshiftException):
    """ error from broker API server. """
    ...

class IllegalRequest(BlueshiftException):
    """ illegal API request. """
    ...

class BrokerError(BlueshiftException):
    """ error raised by broker module. """
    ...

class APIError(BrokerError):
    """ error raised by broker API. """
    ...

class OrderError(BrokerError):
    """ error raised by broker while processing order. """
    ...

class OrderAlreadyProcessed(BrokerError):
    """ error raised while cancelling/ updating order, order already processed. """
    ...

class BrokerConnectionError(BrokerError):
    """ error raised by broker streaming connection. """
    ...

class BadDataError(BrokerError):
    """ bad or malformed data from broker. """
    ...

class AlgoOrderError(BlueshiftException):
    """ error in algo order. """
    ...

class InsufficientFund(BlueshiftException):
    """ insufficient fund to complete order. """
    ...

class TradingControlError(BlueshiftException):
    """ trading control and limits violation error. """
    ...

class NoDataForAsset(BlueshiftException):
    """ no data available for the given asset(s). """
    ...

class NoFurtherDataError(BlueshiftException):
    """ not data available in the window. """
    ...

class HistoryWindowStartsBeforeData(BlueshiftException):
    """ data request for the given asset(s) starts before available. """
    ...

class NoSuchPipeline(BlueshiftException):
    """ pipeline not found. """
    ...