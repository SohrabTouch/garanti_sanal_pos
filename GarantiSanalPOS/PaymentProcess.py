import hashlib

import requests

from fixtures import PosSettings
from Entities import PaymentRequest, Order, Terminal, Customer, Card, Address, OrderItem, Transaction
from Enums import RequestMode, AddressType, CurrencyCode, TransactionType, CardholderPresentCode, MotoInd
from helpers import XmlHelper, HashGenerator


class GarantiPaymentProcess:
    def __init__(self):
        self.settings = PosSettings(RequestMode.Test)
        self.costumer = Customer(self.settings.email_address, self.settings.ip_address)
        self.billing_address = Address(
            'Sohrab',
            'Yavarzadeh',
            AddressType.BILLING_ADDRESS,
            'Kartal',
            'Kartal',
            'Istanbul',
            '+905354837308'
        )
        self.order_item = OrderItem(
            '1',
            '123',
            '456',
            5,
            1000
        )
        self.order = Order(self.costumer, self.billing_address, self.order_item)
        hash_generator = HashGenerator()
        self.hash_data = hash_generator.get_hash_data(
            self.settings.prov_user_password,
            self.settings.terminal_id,
            self.order.order_id,
            self.settings.card.card_number,
            self.order_item.total_amount,
            CurrencyCode.TL
        )
        # self.hash_data = self.generate_hash_data(
        #     self.order.order_id,
        #     self.settings.terminal_id,
        #     self.settings.card.card_number,
        #     self.order_item.total_amount,
        #     CurrencyCode.TL
        # )
        self.terminal = Terminal(
            self.settings.prov_user_id,
            self.settings.user_id,
            self.settings.terminal_id,
            self.settings.merchant_id,
            self.hash_data
        )
        self.transaction = Transaction(
            TransactionType.SALES,
            self.order_item.total_amount,
            CurrencyCode.TL,
            CardholderPresentCode.NORMAL,
            MotoInd.ECommerce,
            None,
            0
        )

    def _generate_security_data(self, data):
        """This method generates a hashed password."""
        sha_data = hashlib.sha1(''.join(data).encode()).hexdigest().upper()
        return sha_data

    def generate_hash_data(self, order_id, terminal_id, card_number, amount, currency_code):
        """This method generates hash data for XML payment."""
        password = self.settings.prov_user_password

        data = [
            password,
            str(terminal_id).rjust(9, '0')  # Ensure terminal_id is left-padded with zeros to 9 digits
        ]

        hashed_password = self._generate_security_data(data)

        hashed_data = [
            str(order_id), str(terminal_id), str(card_number) if card_number else '', str(amount), str(currency_code),
            hashed_password
        ]

        sha_data = hashlib.sha512(''.join(hashed_data).encode()).hexdigest().upper()
        return sha_data

    def create_payment_request_data_xml(self, request: PaymentRequest):
        """
        Creates a dictionary for payment xml data from the request object.

        :param request: The request object containing payment information.
        :return: A dictionary with the payment request data.
        """
        return {
            'Mode': request.mode.value,
            'Version': request.version,
            'Terminal': {
                'ProvUserID': request.terminal.prov_user_id,
                'UserID': request.terminal.user_id,
                'HashData': request.terminal.hash_data,
                'ID': request.terminal.id,
                'MerchantID': request.terminal.merchant_id,
            },
            'Customer': {
                'IPAddress': request.customer.ip_address,
                'EmailAddress': request.customer.email_address,
            },
            'Card': {
                'Number': request.credit_card.card_number,
                'ExpireDate': request.credit_card.get_expire_info(),
                'CVV2': request.credit_card.cvv2,
            },
            'Order': {
                'OrderID': request.order.order_id,
                'GroupID': request.order.group_id
            },
            'Transaction': {
                'Type': request.transaction.type.value,
                'Amount': request.transaction.amount,
                'CurrencyCode': request.transaction.currency_code.value,
                'CardholderPresentCode': request.transaction.cardholder_present_code.value,
                'MotoInd': request.transaction.moto_ind.value
            },
        }

    def prepare_payment(self):
        request = PaymentRequest(
            RequestMode.Test,
            self.settings.version,
            self.terminal,
            self.costumer,
            self.settings.card,
            self.order,
            self.transaction
        )
        request_data = self.create_payment_request_data_xml(request)
        xml_data = XmlHelper.dict_to_xml(request_data, 'GVPSRequest')
        return xml_data

    def pay(self, request_data):
        return self.send(request_data)

    def send(self, data):
        response = requests.post(self.settings.request_url, data=data)
        json_response = XmlHelper.xml_string_to_dict(response.content)
        return json_response['GVPSResponse']
