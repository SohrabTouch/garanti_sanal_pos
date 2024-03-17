import uuid
from Enums import CardholderPresentCode, MotoInd, CurrencyCode, TransactionType, RequestMode
from helpers import generate_random_id


class Card:

    def __init__(self, card_num, holder_name, exp_year, exp_month, cvv2):
        self.card_number = card_num
        self.holder = holder_name
        self.exp_year = exp_year
        self.exp_month = exp_month
        self.cvv2 = cvv2

    def get_expire_info(self):
        return f"{self.exp_year}{int(self.exp_month):02d}"


class AmountInfo:

    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency


class Terminal:

    def __init__(self, prov_user_id: str, user_id: str, identification: str, merchant_id: str, hash_data: str):
        self.prov_user_id = prov_user_id
        self.user_id = user_id
        self.id = identification
        self.merchant_id = merchant_id
        self.hash_data = hash_data


class ThreeDPayment:
    def __init__(self, currency: int, type: str, order_id: str, error_url: str,
                 success_url: str, store_key: str, hashed_password: str, hashed_data: str):
        self.currency = currency
        self.type = type
        self.order_id = order_id
        self.error_url = error_url
        self.success_url = success_url
        self.store_key = store_key
        self.hashed_password = hashed_password
        self.hashed_data = hashed_data


class RewardInfo:
    def __init__(self, _type: str, used_amount: str, gained_amount: str):
        self.type = _type
        self.used_amount = used_amount
        self.gained_amount = gained_amount


class Transaction:
    def __init__(self, transaction_type: TransactionType, amount: str, currency_code: CurrencyCode, cardholder_present_code: CardholderPresentCode,
                 moto_ind: MotoInd, reward_info: RewardInfo = None, installment: int = 0):
        self.type = transaction_type
        self.amount = amount
        self.currency_code = currency_code
        self.cardholder_present_code = cardholder_present_code
        self.moto_ind = moto_ind
        self.installment = "" if installment in [0, 1] else str(installment)
        self.reward = reward_info


class ThreeDPayment:
    def __init__(self, currency: int, _type: str, order_id: str, error_url: str,
                 success_url: str, store_key: str, hashed_password: str, hashed_data: str):
        self.currency = currency
        self.type = _type
        self.order_id = order_id
        self.error_url = error_url
        self.success_url = success_url
        self.store_key = store_key
        self.hashed_password = hashed_password
        self.hashed_data = hashed_data


class OrderItem:
    def __init__(self, number: str, product_id: str, product_code: str, quantity: int, price: float):
        self.number = number
        self.product_id = product_id
        self.product_code = product_code
        self.quantity = quantity
        self.price = price
        self.total_amount = self._get_total_amount(price, quantity)

    @staticmethod
    def _get_total_amount(price, quantity):
        return price * quantity


class Customer:
    def __init__(self, email_address, ip_address):
        self.email_address = email_address
        self.ip_address = ip_address


class Address:
    def __init__(self, first_name, last_name, address_type, address_text, district, city, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.address_type = address_type
        self.address_text = address_text
        self.district = district
        self.city = city
        self.phone_number = phone_number


class OrderComment:
    def __init__(self, number, comment_text):
        self.number = number
        self.comment_text = comment_text


class Recurring:
    def __init__(self, _type, total_payment_num, frequency_type, frequency_interval, start_date, payment_list=None):
        self.type = _type
        self.total_payment_num = total_payment_num
        self.frequency_type = frequency_type
        self.frequency_interval = frequency_interval
        self.start_date = start_date
        self.payment_list = payment_list if payment_list is not None else []


class Order:
    def __init__(self, customer: Customer = None, address: Address = None, item: OrderItem = None,
                 comment: OrderComment = None, recurring: Recurring = None, transaction: Transaction = None):
        self.order_id = self._create_order_number()
        self.group_id = ''
        self.customer = customer  # An instance of the Customer class
        self.address = address  # An instance of the Address class
        self.items = item
        self.comments = comment
        self.recurring = recurring  # An instance of the Recurring class
        self.transaction = transaction  # An instance of the Transaction class, could be linked with RewardInfo,
        # ThreeDPayment, etc.

    def _create_order_number(self):
        # Using uuid4 for generating a unique order ID
        # return 'ef43ef579b97484d9f67d445e4b15b93'
        return generate_random_id()


class PaymentRequest:
    def __init__(self, mode: RequestMode, version: str, terminal: Terminal, customer: Customer,
                 credit_card: Card, order: Order, transaction: Transaction):
        self.mode = mode
        self.version = version
        self.terminal = terminal
        self.customer = customer
        self.credit_card = credit_card
        self.order = order
        self.transaction = transaction