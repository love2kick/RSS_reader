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
    
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
        
class Connector:
    def __init__(self):
        if os.path.exists('./cache')==False:
            os.mkdir('./cache')
        self.dbconnection=sqlite3.connect('cache/cacheDB.db')
        
    def create_table(self, name:str):
        name=name.replace(' ', '_')
        table=f'''CREATE TABLE IF NOT EXISTS {name}(
                TITLE TEXT UNIQUE,
                DATE TEXT,
                LINK TEXT,
                DESCRIPTION TEXT);'''
        with self.dbconnection as con:
            con.cursor().execute(table)
    
    def add_data(self, name:str, title:str, 
                 date:str, link:str, desc:str):
        name=name.replace(' ', '_')
        date=dateconvert(date)
        insert_data_row=(f'INSERT OR IGNORE INTO {name} VALUES (?,?,?,?)')
        with self.dbconnection as con:
            con.cursor().execute(insert_data_row,
                                (title, date, link, desc))
            con.cursor().execute('Commit')
    
    def extract_tables(self) -> list:
        table_list=[]
        with self.dbconnection as con:
            con.row_factory=lambda cursor, row: row[0]
            cursor=con.cursor()
            cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
            for table in cursor.fetchall():
                if table!=None:
                    table_list.append(table)
        return table_list
    
    def extract_data(self, lst:list, date:str):
        date=dateconvert(date)
        with self.dbconnection as con:
            con.row_factory=dict_factory
            cursor=con.cursor()
            for table in lst:
                cursor.execute(f'SELECT TITLE, LINK, DESCRIPTION FROM {table} WHERE DATE="{date}"')
                yield cursor.fetchone()