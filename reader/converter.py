from dict2xml import dict2xml
import lxml.etree as ET
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
import logging

media_path = os.path.join(os.path.dirname(__file__), "media")


def convert_to_xml(entry_dict):
    '''Converts dictionary to xml'''
    logging.info(f'Converting dictionary into xml...')
    xml = ET.fromstring(dict2xml(entry_dict))
    return xml


def convert_to_html(entry_dict):
    '''Applying xsl transformation to an xml 
    in order to form an html file'''
    xml = convert_to_xml(entry_dict)
    logging.info(f'Applying xsl transformation to xml...')
    xslt = ET.parse(os.path.join(media_path, 'xsl/html.xsl'))
    transform = ET.XSLT(xslt)
    result_html = transform(xml)
    logging.info(f'Saving html file...')
    with open(
            os.path.join(
                        media_path,
                        f'{entry_dict["content"]["feed"]}.html'
                        ),
                'wb') as o:
        o.write(ET.tostring(result_html, pretty_print=True))


class PDF_converter(object):
    '''Converts dictionary to pdf'''
    def __init__(self, entry_dict):
        self.dict = entry_dict
        self.converter()

    def converter(self):
        '''Creates a really huge table from result dictionary
        Restrictions: cell shouldn't be bigger than page size'''
        logging.info(f'Converting dictionary into pdf...')
        feedname = self.dict["content"]["feed"]
        pdfpath = os.path.join(media_path,
                               f'./{feedname}.pdf')
        doc = SimpleDocTemplate(pdfpath, pagesize=letter)
        styles = getSampleStyleSheet()
        content = []
        logging.info(f'Adding paragraph with feedname to list...')
        feedpara = f'''<font size="12"><b>
                    Feed: {feedname}
                    </b></font>'''
        paraname = Paragraph(feedpara, styles["Normal"])
        items = self.dict['content']['items']
        tbl_name = [[paraname]]
        tbl = Table(tbl_name, spaceAfter=10)
        content.append(tbl)
        tbl_data = []
        logging.info(f'Creating table with content...')
        for item in items:
            logging.info(f'Adding {items[item]["TITLE"]} to content...')
            title = f'''<font size="10"><i>Title:</i> {items[item]['TITLE']}</font>'''
            paratitle = Paragraph(title, styles["Normal"])
            tbl_data.append([paratitle])
            date = f'''<font size="10"><i>Date:</i> {items[item]['DATE']}</font>'''
            paradate = Paragraph(date, styles["Normal"])
            tbl_data.append([paradate])
            link = f'''<font size="10"><i>Link:</i> {items[item]['LINK']}</font>'''
            paralink = Paragraph(link, styles["Normal"])
            tbl_data.append([paralink])
            desc = f'''<font size="10"><i>Description:</i></font> <font size="8">{items[item]['DESCRIPTION']}</font>'''
            paradesc = Paragraph(desc, styles["Normal"])
            tbl_data.append([paradesc])
            spacer = Spacer(letter[0]-150, 20)
            tbl_data.append([spacer])
        tbl = Table(tbl_data, vAlign='Center', spaceAfter=10)
        content.append(tbl)
        logging.info(f'Building document...')
        doc.build(content)
