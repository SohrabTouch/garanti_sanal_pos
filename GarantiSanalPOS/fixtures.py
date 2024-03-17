from Enums import RequestMode
from Entities import Card


class PosSettings:
    def __init__(self, mode: RequestMode):
        self.request_mode = mode
        self.request_url = self.get_request_url()
        self.version = "512"
        self.prov_user_id = "PROVAUT"
        self.prov_user_id_3ds = "OOS_PAY"
        self.prov_user_password = "123qweASD/"
        self.user_id = "PROVAUT"
        self.terminal_id = "30691297"
        self.merchant_id = "7000679"

        self.email_address = "eticaret@garanti.com.tr"
        self.ip_address = "192.168.0.1"

        self.store_key = "12345678"
        self.three_d_payment_result_url = "http://localhost:8080/gap_php/threed-payment-result.php"
        self.card = Card('5406697543211173', 'Test User', '03', '23', '465')

    def get_request_url(self):
        if self.request_mode == RequestMode.Test:
            self.request_url = "https://sanalposprovtest.garanti.com.tr/VPServlet"
        else:
            self.request_url = "https://sanalposprov.garanti.com.tr/VPServlet"
        return self.request_url