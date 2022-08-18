import args
import req
import re
import logging
import json
from lxml import etree
import xmltodict

args.arguments()

class RSSReader(object):
    """Main reader class.
    It reads from arguments URL link,
    sprinkles some bs4 magic and boom:
    you have an rss feed in your console"""
    def __init__(self, url, limit=0) -> None:
        self.url=url
        if args.limit!=None:
            limit=args.limit
        self.limit=limit
        if args.jtype==False:
            self.run()
        else:
            self.json_run()
        pass
    
    def tag_helper(*string):
        """Removing tags and converting html symbols converted by parser"""
        string=string[1].replace('&lt;','<').replace('&gt;','>')
        return (re.sub('<[^>]*>','', string.replace(r'\n',' ').replace(r'\xa0','')))
    
    def run(self) -> object:
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
            feed=etree.fromstring(req.request_content(self.url))
            #with open('temp/raw.xml','w') as x:
            #    x.writelines(str(etree.tostring(feed, pretty_print=True)))
            print('Feed: ', feed.xpath(".//title/text()")[0]) #print feed name
            logging.info(f'Parsing feed items...')
            for item in feed.xpath(".//item")[:self.limit]:
                title=str(item.xpath("./title/text()"))[2:-2]
                print('\nTitle: ', self.tag_helper(title))
                date=str(item.xpath("./pubdate|pubDate/text()"))[2:-2]
                print('Date: ', self.tag_helper(date))
                link=str(item.xpath("./link/text()"))[2:-2]
                print('Link: ', self.tag_helper(link))
                desc=str(item.xpath("./description/text()"))[2:-2]
                print('Description: ', self.tag_helper(desc))
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
            feed=etree.fromstring(req.request_content(self.url))
            xmlstr=f'<content><Feed>{feed.xpath(".//title/text()")[0]}</Feed><items>'
            logging.info(f'Parsing feed items...')
            for item in feed.xpath(".//item")[:self.limit]: #reassembling xml
                xmlstr+='<item>'
                title=str(item.xpath("./title/text()"))[2:-2]
                xmlstr+='<title>'+self.tag_helper(title).replace('&', '&amp;')+'</title>'
                date=str(item.xpath("./pubdate|pubDate/text()"))[2:-2]
                xmlstr+='<date>'+self.tag_helper(date).replace('&', '&amp;')+'</date>'
                link=str(item.xpath("./link/text()"))[2:-2]
                xmlstr+='<link>'+self.tag_helper(link).replace('&', '&amp;')+'</link>'
                desc=str(item.xpath("./description/text()"))[2:-2]
                xmlstr+='<description>'+self.tag_helper(desc).replace('&', '&amp;')+'</description>'
                xmlstr+='</item>'
            xmlstr+='</items></content>'
            xmldict=xmltodict.parse(xmlstr)
            with open('temp/temp.json', 'w') as e:
                e.writelines(json.dumps(xmldict, indent = 4))
        
if __name__=="__main__":
    r=RSSReader(args.url)
    