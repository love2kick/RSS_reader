from contextlib import contextmanager
from datetime import datetime
import sqlite3
import os
import re

def dateconvert(date):
    if re.match('^[a-zA-Z]+.*', date):
        date=date[5:-15]
        date=datetime.strptime(date,'%d %b %Y').strftime('%Y-%m-%d')
        return date
    else:
        date=datetime.strptime(date,'%Y%m%d').strftime('%Y-%m-%d')
        return date
        
class Connector:
    def __init__(self):
        if os.path.exists('./cache')==False:
            os.mkdir('./cache')
        self.dbcon=sqlite3.connect('cache/cacheDB.db')
        self.dbcursor=self.dbcon.cursor()
        
    @contextmanager
    def create_table(self, name):
        name=name.replace(' ', '_')
        table=f'''CREATE TABLE IF NOT EXISTS {name}(
                TITLE TEXT UNIQUE,
                DATE TEXT,
                LINK TEXT,
                DESCRIPTION TEXT);'''
        self.dbcursor.execute(table)
    
    @contextmanager
    def add_data(self, name, title, 
                 date, link, desc):
        name=name.replace(' ', '_')
        date=dateconvert(date)
        insert_data_row=(f'INSERT OR IGNORE INTO {name} VALUES (?,?,?,?)')
        self.dbcursor.execute(insert_data_row,
                              (title, date, link, desc))
        self.dbcursor.execute('Commit')