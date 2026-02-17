from typing import Dict

import pendulum

from domain.currency_exchange_service.currencies import FiatValue, CurrencyBuilder
from domain.transactions import Transaction
from domain.stock.operations.operation import OperationType


class RowParser:
    OPERATIONS = {
        "BUY - MARKET": OperationType.BUY,
        "BUY - LIMIT": OperationType.BUY,
        "SELL - MARKET": OperationType.SELL,
        "SELL - LIMIT": OperationType.SELL,
        "DIVIDEND": OperationType.DIVIDEND,
        "CUSTODY FEE": OperationType.SERVICE_FEE,
        "STOCK SPLIT": OperationType.STOCK_SPLIT,
    }

    @classmethod
    def parse(cls, row: Dict) -> Transaction:
        raise NotImplementedError

    @classmethod
    def _fiat_value(cls, row: Dict) -> FiatValue:
        currency = CurrencyBuilder.build(row['Currency'])
        # Handles both old format: "-$1,003.01" and new format: "USD 50"
        amount_row = row['Total Amount']
        
        import re
        # Extract digits, dots, and minus sign
        clean_amount = re.sub(r'[^0-9.-]', '', amount_row)
        
        amount = abs(float(clean_amount))
        return FiatValue(amount, currency)

    @classmethod
    def _stock(cls, row: Dict) -> str:
        return row['Ticker']

    @classmethod
    def _date(cls, row: dict) -> pendulum.DateTime:
        return pendulum.parse(row['Date'])

    @classmethod
    def _operation_type(cls, row: dict) -> OperationType:
        return cls.OPERATIONS.get(row['Type'])
