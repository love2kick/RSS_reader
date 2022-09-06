from dict2xml import dict2xml
import lxml.etree as ET
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors


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
    with open(
            os.path.join(
                media_path,
                f'{entry_dict["content"]["feed"]}.html'
            ),
            'wb') as o:
        o.write(ET.tostring(result_html, pretty_print=True))


class PDF_converter(object):

    def __init__(self, entry_dict):
        self.dict = entry_dict
        self.converter()

    def converter(self):
        feedname = self.dict["content"]["feed"]
        pdfpath = os.path.join(media_path,
                               f'./{feedname}.pdf')
        doc = SimpleDocTemplate(pdfpath, pagesize=letter)
        styles = getSampleStyleSheet()
        content = []
        feedpara = f'''<font size="12"><b>
                    Feed: {feedname}
                    </b></font>'''
        paraname = Paragraph(feedpara, styles["Normal"])
        items = self.dict['content']['items']
        tbl_name = [[paraname]]
        tbl = Table(tbl_name, spaceAfter=10)
        content.append(tbl)
        for item in items:
            tbl_data = []
            title = f'''<font size="10">Title: {items[item]['TITLE']}</font>'''
            paratitle = Paragraph(title, styles["Normal"])
            tbl_data.append([paratitle])
            date = f'''<font size="10">Date: {items[item]['DATE']}</font>'''
            paradate = Paragraph(date, styles["Normal"])
            tbl_data.append([paradate])
            link = f'''<font size="10">Link: {items[item]['LINK']}</font>'''
            paralink = Paragraph(link, styles["Normal"])
            tbl_data.append([paralink])
            desc = f'''<font size="10">Description: {items[item]['DESCRIPTION']}</font>'''
            paradesc = Paragraph(desc, styles["Normal"])
            tbl_data.append([paradesc])
            tbl = Table(tbl_data, spaceAfter=10)
            content.append(tbl)

        doc.build(content)
