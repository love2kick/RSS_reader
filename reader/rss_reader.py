import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from reader.dbconnector import Connector
import reader.argums as argums
from reader.helper import (request, request_content, 
                    format_helper, check_url_syntax,
                    xml_checker)
import logging
import json
import xmltodict

argums.arguments()

class RSSReader(object):
    conn=Connector()
    """Main reader class.
    It reads from URL argument link,
    then parses xml string and extracts feed
    into console as direct print or json"""
    def __init__(self) -> None:
        self.url=argums.url
        if argums.limit!=None:  #if --limit doesn't set it takes default value
            self.limit=argums.limit
        else:
            self.limit=None
        if argums.date!=None:
            self.extract_from_base(argums.date)
        else:
            self.url=check_url_syntax(self.url)
            if request(self.url)==200:
                self.feed=xml_checker(request_content(self.url))  #form xml tree from request string
                if argums.jtype==False: #decides which output should go out depending on --json arg
                    self.run()
                else:
                    self.json_run()
    
    def feed_extraction(self, feed, name) -> tuple:
        '''Extracting elements from feed via lovely xpath'''
        logging.info(f'Parsing feed items...')
        for item in feed.xpath(".//item")[:self.limit]:
            title=format_helper(str(item.xpath("./title/text()"))[2:-2])
            date=format_helper(str(item.xpath("./pubdate|pubDate/text()"))[2:-2])
            link=format_helper(str(item.xpath("./link/text()"))[2:-2])
            desc=format_helper(str(item.xpath("./description/text()"))[2:-2])
            self.conn.add_data(name, title, date, link, desc)
            yield title, date, link, desc
                     
    def run(self) -> str:
        """Prints RSS output right in the teminal
        Gets content from URL, 
        parsing for elements and gives and output"""
        feedname=self.feed.xpath(".//title/text()")[0]
        self.conn.create_table(feedname)
        print('Feed: ', feedname)
        for item in self.feed_extraction(self.feed, feedname):
            print('\nTitle:', item[0])
            print('Date:', item[1])
            print('Link:', item[2])
            print('Description:', item[3])
        logging.info(f'Finished!')
            
    def json_run(self) -> json:
        """Creates a dictionary from content and creates a dictionary
        that convertes into json file"""
        feedname=self.feed.xpath(".//title/text()")[0]
        
        xmlstr=('<content><feed>'+
                feedname+
                '</feed><items>')   #forming new xml string from tree
        i=0
        for item in self.feed_extraction(self.feed, feedname):     #further reassembling xml
            xmlstr+=(f'<item_{i}>'+
                        '<title>'+item[0]+'</title>'+
                        '<date>'+item[1]+'</date>'+
                        '<link>'+item[2]+'</link>'+
                        '<description>'+item[3]+'</description>'+
                        f'</item_{i}>')
            i+=1
        xmlstr+='</items></content>'
        logging.info(f'Converting xml into json...')
        jdic=json.dumps(xmltodict.parse(xmlstr), indent = 4)
        print (jdic)
        logging.info(f'Finished!')
    #def extract_from_base(self, date):
        
if __name__=="__main__":
    RSSReader()