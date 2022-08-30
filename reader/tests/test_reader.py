import pytest
from rss_reader import RSSReader
from lxml import etree
import requests
import dbconnector
from unittest.mock import patch
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
    
@pytest.fixture(autouse=True)
def block_db_interactions(monkeypatch):
    class MockedConnector():
        def __init__(self) -> None:
            pass
    monkeypatch.setattr(dbconnector, "Connector", 
                        lambda *args, **kwargs: MockedConnector())
    
@pytest.fixture(autouse=True)
def block_date_convert(monkeypatch):
    def dateconvert():
        pass
    monkeypatch.setattr(dbconnector, "dateconvert", 
                        lambda *args, **kwargs: dateconvert())
@patch('dbconnector.Connector')
class TestReader():
    def test_feed_extraction(self, mocked_get, block_db_interactions, block_date_convert):
        for i in RSSReader().feed_extraction(etree.fromstring(requests.get().content), "name"):
            assert i==('title', 'date', 'link','desc')