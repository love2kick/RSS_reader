import pytest
import coverage
from rss_reader import RSSReader
from lxml import etree
@pytest.fixture
def mocked_reader(monkeypatch):
    class MockedReader():
        def __init__(self):
            self.limit=1
    monkeypatch.setattr(RSSReader, '__init__', 
                        lambda *args, **kwargs: MockedReader())
    
def test_string_formating():
    badstring=r'\n'+'<sometags>\u201cyes\u201d</sometags>'
    assert RSSReader.tag_helper(badstring)=='"yes"'
    
def test_feed_extraction(mocked_reader):
    feed='''<item>
      <title>title</title>
      <description>desc</description>
      <pubDate>date</pubDate>
      <link>link</link>
    </item>'''
    for i in RSSReader.feed_extraction(etree.fromstring(feed)):
        assert i==('title','date', 'link','desc')