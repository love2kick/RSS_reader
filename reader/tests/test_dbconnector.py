import pytest
from dbconnector import Connector, dateconvert

def test_convert_date():
    date1="Wed, 24 Aug 2022 07:05:00 +0000"
    assert dateconvert(date1)=='2022-08-24'