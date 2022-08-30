from contextlib import contextmanager
from datetime import datetime
from email import generator
import sqlite3
import os
import re
import logging

def dateconvert(date):
    '''Converts date from feed and argument to database format'''
    if re.match('^[a-zA-Z]+.*', date):
        date=date[5:-15]
        date=datetime.strptime(date,'%d %b %Y').strftime('%Y-%m-%d')
        return date
    else:
        date=datetime.strptime(date,'%Y%m%d').strftime('%Y-%m-%d')
        return date
    
def dict_factory(cursor, row):
    '''Small function for providing proper row outputs in db'''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
        
class Connector:
    '''Methods of this class are for db interactions.
    They are strongly relying on class initialization.'''
    def __init__(self):
        if os.path.exists('./cache')==False:
            os.mkdir('./cache')
        self.dbconnection=sqlite3.connect('cache/cacheDB.db')
        
    def create_table(self, name:str):
        '''Connects to DB and creates table with feed name if it's not exists'''
        name=name.replace(' ', '_').replace('-','')
        create_table=f'''CREATE TABLE IF NOT EXISTS {name}(
                TITLE TEXT UNIQUE,
                DATE TEXT,
                LINK TEXT,
                DESCRIPTION TEXT);'''
        logging.info(f'Creating table for {name}...')        
        with self.dbconnection as con:
            con.cursor().execute(create_table)
            
    def url_tracker(self, url:str, name:str):
        '''Creates helper table with pairs url-tablename'''
        create_table=f'''CREATE TABLE IF NOT EXISTS url_tracker(
                URL TEXT UNIQUE,
                NAME TEXT);'''
        add_row=f'INSERT OR IGNORE INTO url_tracker VALUES (?,?)'
        url=re.sub(r"https?://(www\.)?",'', url)
        logging.info(f'Creating tracker entry for {name} - {url}...') 
        with self.dbconnection as con:
            cursor=con.cursor()
            cursor.execute(create_table)
            cursor.execute(add_row,
                           (url, name))
            con.cursor().execute('Commit')
            
    def add_data(self, name:str, title:str, 
                 date:str, link:str, desc:str):
        '''Add rows to corresponding table using title as unique entry'''
        name=name.replace(' ', '_').replace('-','')
        date=dateconvert(date)
        insert_data_row=(f'INSERT OR IGNORE INTO {name} VALUES (?,?,?,?)')
        logging.info(f'Creating entries for {name} table...') 
        with self.dbconnection as con:
            con.cursor().execute(insert_data_row,
                                (title, date, link, desc))
            con.cursor().execute('Commit')
    
    def extract_tables(self) -> list:
        '''Extracts table list from db for further parsing'''
        table_list=[]
        logging.info(f'Extracting table list from db...') 
        with self.dbconnection as con:
            con.row_factory=lambda cursor, row: row[0]
            cursor=con.cursor()
            cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
            for table in cursor.fetchall():
                if table!=None and table!='url_tracker':
                    table_list.append(table)
        return table_list
    
    def extract_feed_fromurl(self, url) -> tuple:
        '''This peace of code strips url entry if --date argument given
        and exctracts corresponding feed name'''
        url=re.sub(r"https?://(www\.)?",'', url)
        logging.info(f'Checking tracking entry for {url}...') 
        with self.dbconnection as con:
            cursor=con.cursor()
            cursor.execute(f'SELECT NAME FROM url_tracker WHERE URL="{url}"')
            return cursor.fetchone()
        
    def extract_data(self, target, date:str) -> generator:
        '''Extracts rows in dict format from list excracted from exctract_table method
        or from feed-url provided by user'''
        date=dateconvert(date)
        logging.info(f'Extracting rows for {date}...') 
        with self.dbconnection as con:
            con.row_factory=dict_factory
            cursor=con.cursor()
            if type(target)==list:
                for table in target:
                    cursor.execute(f'SELECT * FROM {table} WHERE DATE="{date}"')
                    yield cursor.fetchall()
            else:
                cursor.execute(f'SELECT * FROM {target} WHERE DATE="{date}"')
                yield cursor.fetchall()