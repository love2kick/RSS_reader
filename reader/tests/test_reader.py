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
    
def test_reader(monkeypatch):
    def block_db_interactions():
        pass
    monkeypatch.setattr('dbconnector.Connector.add_data', block_db_interactions())
    
    def test_feed_extraction(mocked_get):
        for i in RSSReader.feed_extraction(etree.fromstring(requests.get().content), "name"):
            assert i==('title', 'date', 'link','desc')