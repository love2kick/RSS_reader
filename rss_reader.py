import args
import req
from bs4 import BeautifulSoup as bs
import re

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
        if self.url.startswith("http")==False:
            print(f"{self.url} doesn't have required prefix. Trying to add one.")
            self.url="http://"+self.url
        if req.request(self.url)==200:
            soup=bs(req.request_content(self.url), 'xml')
            items=soup.find_all(['item'], limit=args.limit)
            for item in items:
                print('\n')
                for i in item.find_all(['title', 'pubDate','link']):
                    print(re.sub('<[^>]*>','', str(i)))
            
        
if __name__=="__main__":
    r=RSSReader(args.url)