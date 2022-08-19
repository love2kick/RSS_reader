import args
import req
import re
import logging
import json
import unicodedata
from bs4 import BeautifulSoup
from lxml import etree
import xmltodict

args.arguments()

class RSSReader(object):
    """Main reader class.
    It reads from arguments URL link,
    sprinkles some magic and boom:
    you have an rss feed in your console/.json file"""
    def __init__(self, url, limit=None) -> None:
        self.url=url
        if args.limit!=None: #if --limit doesn't set it takes default value -1
            limit=args.limit
        self.limit=limit
        if args.jtype==False: #decides which output should go out depending on --json arg
            self.run()
        else:
            self.json_run()
        pass
    
    @classmethod
    def tag_helper(self, string) -> str:
        """Removing tags and converting html/unicode symbols"""
        string = str(BeautifulSoup(string, 'html.parser'))       
        string=(re.sub('<[^>]*>','', string))                   #removing excessive tags
        string=string.replace(r'\n','')                          #replacing unnecessary newlines
        string=(string.replace(u'\u2019', '\'').
                replace(u'\u2026','...').replace(r'\\','').
                replace(u'\u201c','\"').replace(u'\u201d','\"').
                replace(u'\xa0', ' ').replace(u'\u2014', '-').   #string below doesn't convert some unicode chars
                replace(u'\u2018', '\''))                        #and this is why this part exists, FUUUUUU
        string=unicodedata.normalize('NFKD', string)
        return string
    
    @classmethod
    def feed_extraction(self,feed):
        '''Extracting elements from feed via lovely xpath'''
        for item in feed.xpath(".//item")[:self.limit]:
            title=self.tag_helper(str(item.xpath("./title/text()"))[2:-2])
            date=self.tag_helper(str(item.xpath("./pubdate|pubDate/text()"))[2:-2])
            link=self.tag_helper(str(item.xpath("./link/text()"))[2:-2])
            desc=self.tag_helper(str(item.xpath("./description/text()"))[2:-2])
            yield title, date, link, desc
               
    def run(self) -> str:
        """Prints RSS output right in the teminal
        Gets content from URL, 
        parsing for elements and gives and output"""
        logging.info(f'Checking URL...')
        if self.url.startswith("http")==False:
            print(f"{self.url} doesn't have required prefix. Trying to add one.")
            self.url="http://"+self.url
        logging.info(f'Checking connection to {self.url}...')
        if req.request(self.url)==200:
            logging.info(f'Scrapping data from feed...')
            feed=etree.fromstring(req.request_content(self.url)) #form xml tree from request string
            print('Feed: ', feed.xpath(".//title/text()")[0]) #prints feed name
            logging.info(f'Parsing feed items...')
            for item in self.feed_extraction(feed):
                print('\nTitle:', item[0])
                print('Date:', item[1])
                print('Link:', item[2])
                print('Description:', item[3])
            logging.info(f'Finished!')
            
    def json_run(self) -> json:
        """Creates a dictionary from content and creates a dictionary
        that convertes into json file"""
        logging.info(f'Checking URL...')
        if self.url.startswith("http")==False:
            print(f"{self.url} doesn't have required prefix. Trying to add one.")
            self.url="http://"+self.url
        logging.info(f'Checking connection to {self.url}...')
        if req.request(self.url)==200:
            logging.info(f'Scrapping data from feed...')
            feed=etree.fromstring(req.request_content(self.url)) #form xml tree from request string
            xmlstr=f'<content><Feed>{feed.xpath(".//title/text()")[0]}</Feed><items>' #forming new xml string from tree
            logging.info(f'Parsing feed items and reassembling xml string...')
            i=0
            for item in self.feed_extraction(feed):     #further reassembling xml
                xmlstr+=f'<item_{i}>'
                xmlstr+='<title>'+item[0]+'</title>'
                xmlstr+='<date>'+item[1]+'</date>'
                xmlstr+='<link>'+item[2]+'</link>'
                xmlstr+='<description>'+item[3]+'</description>'
                xmlstr+=f'</item_{i}>'
                i+=1
            xmlstr+='</items></content>'
            logging.info(f'Converting xml into dictionary...')
            xmldict=xmltodict.parse(xmlstr)
            logging.info(f'Converting dictionary into json and writin into file...')
            jdic=json.dumps(xmldict, indent = 4)
            with open('temp/temp.json', 'w') as e:
                e.writelines(jdic)
            logging.info(f'Finished!')
            return jdic
        
if __name__=="__main__":
    r=RSSReader(args.url)
    