import requests
import unicodedata
import re
from lxml import etree
from bs4 import BeautifulSoup

def request(url):
    '''checks request status code, returns code value'''
    r=requests.get(url)
    code=r.status_code
    try:
        if code!=200:
            raise ConnectionError
        else:
            return code
    except ConnectionError:
        print(f"Request status code not 200 (code: {code}). Exiting")
        raise SystemExit()
    
def request_content(url):
    '''returns requests content'''
    r=requests.get(url)
    return r.content

def format_helper(string) -> str:
    '''Removing tags and unicode/html junk'''
    string = str(BeautifulSoup(string, 'lxml'))
    string = unicodedata.normalize('NFKD', string)   
    string = (re.sub('<[^>]*>','', string))                  #removing excessive tags
    string=string.replace(r'\n','')                          #replacing unnecessary newlines
    string=(string.replace(u'\u2019', '\'').
            replace(u'\u2026','...').replace(u'\u201c','\"').
            replace(u'\u201d','\"').replace(r'\xa0', ' ').
            replace(u'\u2013', '-').replace(u'\u2013', '-').
            replace(u'\u2014', '-').replace(u'\u2018', '\'').#string above cannot convert some unicode chars
            replace('\\',' ').replace(u'\u0301','\''))      #and this is why this part exist FUUUUUU
    return string

def check_url_syntax(url:str)->str:
    '''Checking url syntax and trying to fix it'''
    try:
        if url.startswith("http")==False:
            raise Exception("Wrong url syntax!")
    except Exception:
            print(f"{url} doesn't have required prefix. Trying to add one.")
            url="http://"+url
    finally:
        return url

def xml_checker(feed):
    '''Tries to convert string to xml'''
    try:
        xml=etree.fromstring(feed)
        return xml
    except etree.XMLSyntaxError:
        print("XML doesn't well formed.")
        raise SystemExit()