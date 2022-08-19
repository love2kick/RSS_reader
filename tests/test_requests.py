import pytest
import coverage
import req
import requests

@pytest.fixture()
def return_content(monkeypatch):
    class MockedGet():
        def __init__(self) -> None:
            self.content="This is content!"
            self.status_code=404
    monkeypatch.setattr(requests, "get", 
                        lambda *args, **kwargs: MockedGet())
    
def test_request_normallink():
    '''INTERNET CONNECTION REQUIRED FOR THIS TEST'''
    assert req.request('http://google.com') == 200

def test_return_content(return_content):
    assert req.request_content(return_content)=="This is content!"

def test_connection_error_exception(return_content):
    with pytest.raises(SystemExit):
        req.request(return_content)
