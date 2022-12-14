import pytest
import helper
import requests
from dbconnector import Connector

@pytest.fixture()
def return_content(monkeypatch):
    class MockedGet():
        def __init__(self) -> None:
            self.content="This is content!"
            self.status_code=404
    monkeypatch.setattr(requests, "get", 
                        lambda *args, **kwargs: MockedGet())
    
@pytest.fixture()
def block_db_interactions(monkeypatch):
    class MockedConnector():
        pass
    monkeypatch.setattr(Connector, "__init__", 
                        lambda *args, **kwargs: MockedConnector())
    
     
def test_request_normallink():
    '''INTERNET CONNECTION REQUIRED FOR THIS TEST'''
    assert helper.request('https://google.com') == 200

def test_return_content(return_content):
    assert helper.request_content(return_content)=="This is content!"

def test_connection_error_exception(return_content):
    with pytest.raises(SystemExit):
        helper.request(return_content)
        
def test_string_formating():
        badstring=r'\n'+'<sometags>\u201cyes\u201d</sometags>'
        assert helper.format_helper(badstring)=='"yes"'
        
def test_xml_checker():
        badxml='''<root><title>roottitle<title></root>'''
        with pytest.raises(SystemExit):
            helper.xml_checker(badxml)