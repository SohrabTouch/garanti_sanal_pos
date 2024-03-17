import xml.etree.ElementTree as ET
from hashlib import sha1
from xml.dom.minidom import parseString


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
        root = ET.fromstring(xml_string)

        def element_to_dict(element):
            return {element.tag: {child.tag: child.text for child in element} or element.text}

        return element_to_dict(root)

