import args
import requests
from bs4 import BeautifulSoup as bs
verb = args.verb
args.arguments()

class RSSReader(object):
    """Default text"""
    def __init__(self, url, limit=0) -> None:
        self.url=url
        if args.limit!=None:
            limit=args.limit
        self.limit=limit
        self.run()
        pass
    
    def run(self) -> object:
        if self.url.startswith("http")==False:
            print(f"{self.url} doesn't have required prefix. Trying to add one.")
            self.url="http://"+self.url
        r=requests.get(self.url)
        if r.status_code==200:
            soup=bs(r.content, 'html.parser')
            print(soup.prettify())
        
if __name__=="__main__":
    r=RSSReader(args.url)