import pytest
from rss_reader import RSSReader
from lxml import etree
import requests
import dbconnector

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
    
@pytest.fixture()
def mocked_connector(monkeypatch):
    class MockedConnector():
        pass
    monkeypatch.setattr(dbconnector.Connector, "get", 
                        lambda *args, **kwargs: MockedConnector())
    
class TestReader():
    def test_feed_extraction(self, mocked_get, mocked_connector):
        for i in RSSReader().feed_extraction(etree.fromstring(requests.get().content), "name"):
            assert i==('title', 'date', 'link','desc')