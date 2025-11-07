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
import numpy

from ..term import LoadableTerm
from ..factors.factors import Factor


class Column(LoadableTerm):
    """column of pipeline computation. """
    ...

class BoundColumn(Column):
    """ column of data computation, associated with a dataset. """
    name:str
    qualname:str
    dtype:numpy.dtype
    latest:Factor # mostly relevant for factors, but can be for any

class DataSetMeta:
    """ a metaclass for dataset. """
    columns:frozenset
    qualname:str

class DataSet(DataSetMeta):
    """ a dataset. """
    ...

class EquityPricing(DataSet):
    """ Equity pricing columns. """
    open:BoundColumn
    high:BoundColumn
    low:BoundColumn
    close:BoundColumn
    volume:BoundColumn

class FnOPricing(DataSet):
    """ Futures and options pricing columns. """
    open:BoundColumn
    high:BoundColumn
    low:BoundColumn
    close:BoundColumn
    open_interest:BoundColumn

class QuarterlyFundamental(DataSet):
    """ company quarterly fundamental data. """
    operating_income:BoundColumn
    cogs:BoundColumn
    employee_expenses:BoundColumn
    rnd_expenses:BoundColumn
    sgna_expenses:BoundColumn
    operating_expenses:BoundColumn
    operating_profit:BoundColumn
    other_income:BoundColumn
    total_revenue:BoundColumn
    extraordinary_items:BoundColumn
    provisions:BoundColumn
    total_expenses:BoundColumn
    ebitda:BoundColumn
    depreciation:BoundColumn
    ebit:BoundColumn
    interest:BoundColumn
    pbt:BoundColumn
    tax:BoundColumn
    pat:BoundColumn
    eps:BoundColumn
    face_value:BoundColumn
    number_of_shares:BoundColumn
    capital_adequacy_ratio:BoundColumn
    gross_npa:BoundColumn
    gross_npa_pct:BoundColumn
    net_npa:BoundColumn
    net_npa_pct:BoundColumn

class AnnualFundamental(DataSet):
    """ company annual fundamentals. """
    share_capital:BoundColumn
    reservers_and_surpluses:BoundColumn
    total_equity:BoundColumn
    lt_debt:BoundColumn
    st_debt:BoundColumn
    current_liabilities:BoundColumn
    borrowings:BoundColumn
    deposits:BoundColumn
    non_current_liabilities:BoundColumn
    total_capital_liabilities:BoundColumn
    tangible_assets:BoundColumn
    intangible_assets:BoundColumn
    cwip:BoundColumn
    fixed_assets:BoundColumn
    non_current_assets:BoundColumn
    cash:BoundColumn
    inventories:BoundColumn
    investments:BoundColumn
    advances:BoundColumn
    interbank_loans:BoundColumn
    current_assets:BoundColumn
    total_assets:BoundColumn
    equity_capital:BoundColumn
    ev:BoundColumn
    gross_npa:BoundColumn
    net_npa:BoundColumn
    number_of_shares:BoundColumn
    operating_income:BoundColumn
    other_income:BoundColumn
    total_revenue:BoundColumn
    cogs:BoundColumn
    employee_expenses:BoundColumn
    operating_expenses:BoundColumn
    provisions:BoundColumn
    extraordinary_items:BoundColumn
    total_expenses:BoundColumn
    operating_profit:BoundColumn
    ebitda:BoundColumn
    depreciation:BoundColumn
    ebit:BoundColumn
    interest:BoundColumn
    pbt:BoundColumn
    tax:BoundColumn
    pat:BoundColumn
    cff:BoundColumn
    cfi:BoundColumn
    cfo:BoundColumn
    eps:BoundColumn
    ceps:BoundColumn
    bvps:BoundColumn
    rps:BoundColumn
    roa:BoundColumn
    roce:BoundColumn
    roe:BoundColumn
    ev_to_ebitda:BoundColumn
    ev_to_sales:BoundColumn
    pb:BoundColumn
    ps:BoundColumn
    earning_yield:BoundColumn
    dividend_payout_ratio:BoundColumn
    ebitda_margin:BoundColumn
    npm:BoundColumn
    opm:BoundColumn
    debt_to_equity:BoundColumn
    lt_debt_to_equity:BoundColumn
    interest_coverage:BoundColumn
    inventory_turnover_ratio:BoundColumn
    quick_ratio:BoundColumn
    current_ratio:BoundColumn
    asset_turnover_ratio:BoundColumn
    nim:BoundColumn
    cir:BoundColumn
    net_npa_pct:BoundColumn
    gross_npa_pct:BoundColumn

class EquitySector(DataSet):
    sector:BoundColumn

__all__ = [
    'BoundColumn',
    'Column',
    'DataSet',
    'EquityPricing',
    'FnOPricing',
    'QuarterlyFundamental',
    'AnnualFundamental',
    'EquitySector',
]