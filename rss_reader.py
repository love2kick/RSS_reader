import args
import req
from bs4 import BeautifulSoup as bs
import re
import logging

args.arguments()
verb = args.verb
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
        self.run()
        pass
    
    def run(self) -> object:
        """"Meaningful comment, SOON"""
        logging.info(f'Checking URL...')
        if self.url.startswith("http")==False:
            print(f"{self.url} doesn't have required prefix. Trying to add one.")
            self.url="http://"+self.url
        logging.info(f'Checking connection to {self.url}...')
        if req.request(self.url)==200:
            logging.info(f'Scrapping data from feed...')
            soup=bs(req.request_content(self.url), 'xml')
            items=soup.find_all(['item'], limit=self.limit)
            logging.info(f'Parsing feed items...')
            for item in items:
                print('\n')
                for i in item.find_all(['title', 'pubDate','link']):
                    print(re.sub('<[^>]*>','', str(i)))
            logging.info(f'Finished!')
            
        
if __name__=="__main__":
    r=RSSReader(args.url)
    