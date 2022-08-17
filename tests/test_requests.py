import pytest
import coverage
import req


def test_request_function():
    assert req.request('https://news.yahoo.com/rss/') == 200