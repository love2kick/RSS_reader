import pytest
from rss_reader import RSSReader
from lxml import etree
import requests

@pytest.fixture()
def mocked_get(monkeypatch):
    class MockedGet():
        def __init__(self) -> None:
            self.content='''<root>
            <title>roottitle</title>
            <items><item>
            <title>title</title>
            <description>desc</description>
            <pubDate>date</pubDate>
            <link>link</link>
            </item></items>
            </root>'''
            self.status_code=200
    monkeypatch.setattr(requests, "get", 
                        lambda *args, **kwargs: MockedGet())
    
class TestReader():
    def test_feed_extraction(self, mocked_get):
        for i in RSSReader().feed_extraction(etree.fromstring(requests.get().content), "name"):
            assert i==('title', 'date', 'link','desc')