import pytest
import coverage
import req
import requests
import pytest_mock

@pytest.fixture()
def return_content(monkeypatch):
    class MockedGet():
        def __init__(self) -> None:
            self.content="This is content!"
            self.status_code=200
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockedGet())
    
def test_request_normallink(return_content):
    assert req.request(return_content) == 200

def test_return_content(return_content):
    assert req.request_content(return_content)=="This is content!"

