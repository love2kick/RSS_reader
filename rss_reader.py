from args import arguments
import requests

arguments()

class RSSReader(object):
    """Default text"""
    def __init__(self, url, limit) -> None:
        self.url=url
        self.limit=limit
        pass
    
   #def get_feed(self) -> object:
        