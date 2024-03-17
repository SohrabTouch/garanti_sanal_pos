from enum import Enum


class RequestMode(Enum):
    Test = 'TEST'
    Prod = 'PROD'


class MotoInd(Enum):
    ECommerce = 'N'
    Moto = 'Y'
    H = 'H'


class CurrencyCode(Enum):
    TL = 949
    USD = 840
    EURO = 978
    GBP = 826
    JPY = 392


class RewardType(Enum):
    BNS = 'BNS'
    FBB = 'FBB'


class TransactionType(Enum):
    SALES = "sales"
    VOID = "void"
    REFUND = "refund"
    PRE_AUTH = "preauth"
    POST_AUTH = "postauth"
    PARTIAL_VOID = "partialvoid"
    ORDER_INQUIRY = "orderinq"
    ORDER_HISTORY_INQUIRY = "orderhistoryinq"
    ORDER_LIST_INQ = "orderlistinq"
    BONUS_INQ = "rewardinq"
    DCC = "dccinq"


class CardholderPresentCode(Enum):
    NORMAL = "0"
    SECURE_3D = "13"


class AddressType(Enum):
    SHIPPING_ADDRESS = "S"
    BILLING_ADDRESS = "B"