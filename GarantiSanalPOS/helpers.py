import hashlib
import random
import xml.etree.ElementTree as ET
from hashlib import sha1
from xml.dom.minidom import parseString
import xmltodict


class PriceFormatter:
    @staticmethod
    def format_amount(amount):
        return round(amount, 2) * 100


class XmlHelper:
    @staticmethod
    def dict_to_xml(data, root_element='root'):
        def build_element(parent, structure):
            if isinstance(structure, dict):
                for key, value in structure.items():
                    sub_element = ET.SubElement(parent, key)
                    build_element(sub_element, value)
            else:
                parent.text = str(structure)

        root = ET.Element(root_element)
        build_element(root, data)
        # Generate the XML string with the declaration, specifying the 'iso-8859-9' encoding
        xml_str = ET.tostring(root, encoding='iso-8859-9', xml_declaration=True)
        # Use minidom for pretty printing
        return parseString(xml_str).toprettyxml(encoding='iso-8859-9').decode('iso-8859-9')

    @staticmethod
    def xml_string_to_dict(xml_string):
        return xmltodict.parse(xml_string)
        # root = ET.fromstring(xml_string)
        #
        # def element_to_dict(element):
        #     return {element.tag: {child.tag: child.text for child in element} or element.text}

        return element_to_dict(root)


class HashGenerator:
    def __init__(self, charset='ISO-8859-9'):
        self.charset = charset

    def calculate_hash(self, data, algorithm):
        """
        Generic method to calculate hash of the given data using the specified algorithm.
        """
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(data.encode(self.charset))
        return hash_obj.hexdigest().upper()

    def sha1(self, data):
        """
        Calculate SHA-1 hash of the given data.
        """
        return self.calculate_hash(data, 'sha1')

    def sha512(self, data):
        """
        Calculate SHA-512 hash of the given data.
        """
        return self.calculate_hash(data, 'sha512')

    def get_hash_data(self, user_password, terminal_id, order_id, card_number, amount, currency_code):
        """
        Generate hash data combining various parameters with hashed password.
        """
        hashed_password = self.sha1(user_password + "0" + terminal_id)
        hash_data = self.sha512(order_id + terminal_id + card_number + str(amount) + str(currency_code.value) + hashed_password)
        return hash_data


def generate_random_id():
    parts = [
        random.randint(0, 65535),
        random.randint(0, 65535),
        random.randint(0, 65535),
        random.randint(16384, 20479),
        random.randint(32768, 49151),
        random.randint(0, 65535),
        random.randint(0, 65535),
        random.randint(0, 65535)
    ]
    # Using '{:04X}' to format integers as 4-character hexadecimal strings, similar to '%04X' in PHP
    return ''.join('{:04X}'.format(part) for part in parts)