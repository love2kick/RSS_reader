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
    """Main reader class.
    It reads from URL argument link,
    then parses xml string and extracts feed
    into console as direct print or json"""
    def __init__(self) -> None:
        self.conn=Connector()
        self.url=argums.url
        self.limit=argums.limit
        if argums.date!=None:
            if argums.jtype==False:
                self.run(self.extract_from_db(argums.date))
            else:
                self.json_run(self.extract_from_db(argums.date))
        else:
            self.url=check_url_syntax(self.url) #checking url syntax and adding http:// if needed
            if request(self.url)==200:
                self.feed=xml_checker(request_content(self.url))  #form xml tree from request content
                if argums.jtype==False:
                    self.run()
                else:
                    self.json_run()
    
    def feed_extraction(self, feed, name) -> tuple:
        '''Extracting elements from feed via lovely xpath'''
        logging.info(f'Scrapping data from feed...')
        logging.info(f'Parsing feed items...')
        for item in feed.xpath(".//item")[:self.limit]:
            title=format_helper(str(item.xpath("./title/text()"))[2:-2])
            date=format_helper(str(item.xpath("./pubdate|pubDate/text()"))[2:-2])
            link=format_helper(str(item.xpath("./link/text()"))[2:-2])
            desc=format_helper(str(item.xpath("./description/text()"))[2:-2])
            self.conn.add_data(name, title, date, link, desc)
            yield title, date, link, desc
            
    def tables_creation(self, url, name):
        '''Create tables if needed, adds url-feedname pair'''
        self.conn.create_table(name)
        self.conn.url_tracker(url, name)
        
    def run(self, entry_dict=None) -> sys.stdout:
        """Prints RSS output right in the teminal
        Gets content from URL, 
        parsing for elements and gives and output"""
        if entry_dict==None:
            feedname=self.feed.xpath(".//title/text()")[0]
            self.tables_creation(self.url,feedname)
            print('Feed: ', feedname)
            for item in self.feed_extraction(self.feed, feedname):
                print('\nTitle:', item[0])
                print('Date:', item[1])
                print('Link:', item[2])
                print('Description:', item[3])
        else:
            print(entry_dict['content']['feed'])
            items=entry_dict['content']['items']
            for item in items:
                print('\nTitle', items[item]['TITLE'])
                print('Date:', items[item]['DATE'])
                print('Link:', items[item]['LINK'])
                print('Description:', items[item]['DESCRIPTION'])
            
        logging.info(f'Finished!')
            
    def json_run(self, entry_dict=None) -> sys.stdout:
        """Creates a dictionary from content and creates a dictionary
        that convertes into json file"""
        if entry_dict==None:
            feedname=self.feed.xpath(".//title/text()")[0]
            self.conn.create_table(feedname)
            xmlstr=('<content><feed>'+
                    feedname+
                    '</feed><items>')   #form new xml string from tree
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
            result_dict=xmltodict.parse(xmlstr)
        else:
            result_dict=entry_dict
        jdict=json.dumps(result_dict, indent = 4)
        print (jdict)
        logging.info(f'Finished!')
        
    def extract_from_db(self, date):
        '''Extracts data from db as dictionary'''
        result_dict={'content':{'feed':None,'items':{}}}
        if self.url!=None:
            name_from_url=self.conn.extract_feed_fromurl(self.url)
            for item_list in self.conn.extract_data(name_from_url[0], date):
                result_dict['content']['feed']=name_from_url[0]
                for item, i in zip(item_list, range(len(item_list))):
                    if i!=self.limit:
                        result_dict['content']['items'].update({f'item{i}':item})
            return result_dict
        else:
            tables=self.conn.extract_tables()
            result_dict['content']['feed']=[]
            result_list=[]
            for item_list, table in zip(self.conn.extract_data(tables,date), tables):
                if item_list!=None and item_list!=[]:
                    result_dict['content']['feed'].append(table)
                    for item in item_list:
                        result_list.append(item)
            for dictionary, i in zip(result_list, range(len(result_list))):
                if i!=self.limit:
                    result_dict['content']['items'].update({f'item{i}':dictionary})
            return result_dict
                    
        
if __name__=="__main__":
    RSSReader()