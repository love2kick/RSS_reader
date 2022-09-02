from dict2xml import dict2xml
import lxml.etree as ET
import os
media_path = os.path.join(os.path.dirname(__file__), "media")


def convert_to_xml(entry_dict):
    '''Converts dictionary to xml'''
    xml = ET.fromstring(dict2xml(entry_dict))
    return xml


def convert_to_html(entry_dict):
    '''Applying xsl transformation to an xml 
    in order to form an html file'''
    xml = convert_to_xml(entry_dict)
    xslt = ET.parse(os.path.join(media_path, 'xsl/html.xsl'))
    transform = ET.XSLT(xslt)
    result_html = transform(xml)
    with open(os.path.join(media_path, f'{str(xml.xpath(".//feed/text()"))[2:-2]}.html'), 'wb') as o:
        o.write(ET.tostring(result_html, pretty_print=True))
