from dict2xml import dict2xml
import lxml.etree as ET
from lxml import objectify
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from decimal import Decimal


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
            f'{entry_dict["content"]["feed"][0]}.html'
            ),
        'wb') as o:
        o.write(ET.tostring(result_html, pretty_print=True))

def convert_to_pdf(entry_dict):
    pdfpath = os.path.join(media_path,
                           f'./{entry_dict["content"]["feed"][0]}.pdf')
    pass
    
class PDF_converter(object):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, entry_dict):
        """Constructor"""
        self.entry_dict = entry_dict
        self.pdf_file = os.path.join(media_path,
                           f'./{entry_dict["content"]["feed"][0]}.pdf')
        
        self.xml = convert_to_xml(entry_dict)
        
    #----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        # http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height -  y * unit
        return x, y  
        
    #----------------------------------------------------------------------
    def createPDF(self):
        """
        Create a PDF based on the XML data
        """
        self.canvas = canvas.Canvas(self.pdf_file, pagesize=letter)
        width, self.height = letter
        styles = getSampleStyleSheet()
        xml = self.xml
        
        feedname = """ <font size="12">
        Feedname:%s<br>
        </font>
        """ % (xml.address1, xml.address2, xml.address3, xml.address4)
        p = Paragraph(feedname, styles["Normal"])
        p.wrapOn(self.canvas, width, self.height)
        p.drawOn(self.canvas, *self.coord(18, 40, mm))
        
        order_number = '<font size="14"><b>Order #%s </b></font>' % xml.order_number
        p = Paragraph(order_number, styles["Normal"])
        p.wrapOn(self.canvas, width, self.height)
        p.drawOn(self.canvas, *self.coord(18, 52, mm))
        
        data = []
        data.append(["Item ID", "Name", "Price", "Quantity", "Total"])
        grand_total = 0
        for item in xml.order_items.iterchildren():
            row = []
            row.append(item.id)
            row.append(item.name)
            row.append(item.price)
            row.append(item.quantity)
            total = Decimal(str(item.price)) * Decimal(str(item.quantity))
            row.append(str(total))
            grand_total += total
            data.append(row)
        data.append(["", "", "", "Grand Total:", grand_total])
        t = Table(data, 1.5 * inch)
        t.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black)
        ]))
        t.wrapOn(self.canvas, width, self.height)
        t.drawOn(self.canvas, *self.coord(18, 85, mm))
        
        txt = "Thank you for your business!"
        p = Paragraph(txt, styles["Normal"])
        p.wrapOn(self.canvas, width, self.height)
        p.drawOn(self.canvas, *self.coord(18, 95, mm))
    
    #----------------------------------------------------------------------
    def savePDF(self):
        """
        Save the PDF to disk
        """
        self.canvas.save()