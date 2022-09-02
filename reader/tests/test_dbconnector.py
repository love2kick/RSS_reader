import pytest
from dbconnector import Connector, dateconvert


def test_convert_date():
    date1 = "Wed, 10 May 1945 07:05:00 +0000"
    date2 = '19450510'
    assert dateconvert(date1) == '1945-05-10'
    assert dateconvert(date2) == '1945-05-10'


class Test_db_interactions():
    conn = Connector()
    test_table = 'TESTTABLE'
    url = 'https://www.TEST'
    title = 'TestTitle'
    date = "Wed, 10 May 1945 07:05:00 +0000"
    desc = 'SomeRandomDescription'
    test_dict = {'TITLE': title,
                 'DATE': '1945-05-10',
                 'LINK': url,
                 'DESCRIPTION': desc}

    def test_table_creation_extraction(self):
        self.conn.create_table(self.test_table)
        table_list = self.conn.extract_tables()
        assert self.test_table in table_list

    def test_add_test_url(self):
        name = '-TEST TEST-'
        self.conn.url_tracker(self.url, name)
        from_url = self.conn.extract_feed_fromurl(self.url)
        assert from_url == 'TEST_TEST'

    def test_write_and_extract_row(self):

        self.conn.add_data(self.test_table, self.title,
                           self.date, self.url, self.desc)
        extracted_row = list
        for item in self.conn.extract_data(self.test_table, self.date):
            extracted_row = item
        assert extracted_row[0] == self.test_dict

    def test_extract_row_by_date(self):
        table_list = self.conn.extract_tables()
        extracted_row = dict
        for item in self.conn.extract_data(table_list, self.date):
            extracted_row = item
        assert extracted_row[0] == self.test_dict

    def test_cleanup(self):
        cursor = self.conn.dbconnection.cursor()
        cursor.execute(f'DROP TABLE {self.test_table}')
        cursor.execute(f'DELETE FROM url_tracker WHERE url="TEST"')
        cursor.execute('Commit')
        table_list = self.conn.extract_tables()
        assert self.test_table not in table_list
        from_url = self.conn.extract_feed_fromurl(self.url)
        assert from_url == None
