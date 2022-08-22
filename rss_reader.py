import args
from helper import (request, request_content, 
                    format_helper, check_url_syntax,
                    xml_checker)
import logging
import json
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
        if args.limit!=None:  #if --limit doesn't set it takes default value -1
            limit=args.limit
        self.limit=limit
        if args.jtype==False: #decides which output should go out depending on --json arg
            self.run()
        else:
            self.json_run()
    
    def feed_extraction(self, feed) -> tuple:
        '''Extracting elements from feed via lovely xpath'''
        for item in feed.xpath(".//item")[:self.limit]:
            title=format_helper(str(item.xpath("./title/text()"))[2:-2])
            date=format_helper(str(item.xpath("./pubdate|pubDate/text()"))[2:-2])
            link=format_helper(str(item.xpath("./link/text()"))[2:-2])
            desc=format_helper(str(item.xpath("./description/text()"))[2:-2])
            yield title, date, link, desc
                     
    def run(self) -> str:
        """Prints RSS output right in the teminal
        Gets content from URL, 
        parsing for elements and gives and output"""
        logging.info(f'Checking URL...')
        self.url=check_url_syntax(self.url)
        logging.info(f'Checking connection to {self.url}...')
        if request(self.url)==200:
            logging.info(f'Scrapping data from feed...')
            feed=xml_checker(request_content(self.url))    #form xml tree from request string
            print('Feed: ', feed.xpath(".//title/text()")[0])   #prints feed name
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
        self.url=check_url_syntax(self.url)
        logging.info(f'Checking connection to {self.url}...')
        if request(self.url)==200:
            logging.info(f'Scrapping data from feed...')
            feed=xml_checker(request_content(self.url))    #form xml tree from request string
            xmlstr=('<content><feed>'+
                    feed.xpath(".//title/text()")[0]+
                    '</feed><items>')   #forming new xml string from tree
            logging.info(f'Parsing feed items and reassembling xml string...')
            i=0
            for item in self.feed_extraction(feed):     #further reassembling xml
                xmlstr+=(f'<item_{i}>'+'<title>'+item[0]+'</title>'+
                         '<date>'+item[1]+'</date>'+'<link>'+item[2]+'</link>'+
                         '<description>'+item[3]+'</description>'+
                         f'</item_{i}>')
                i+=1
            xmlstr+='</items></content>'
            logging.info(f'Converting xml into dictionary...')
            xmldict=xmltodict.parse(xmlstr)
            logging.info(f'Converting dictionary into json and writin into file...')
            jdic=json.dumps(xmldict, indent = 4)
            print (jdic)
            logging.info(f'Finished!')
            return jdic
        
if __name__=="__main__":
    r=RSSReader(args.url)