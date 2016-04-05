__author__ = 'king'
import sqlite3
import md5

author_creator = '''CREATE TABLE QSBK_AUTHOR
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT,
       STATUS            INT     NOT NULL,
       UPDATE_TIME         INT);'''

joke_creator = '''CREATE TABLE JOKE
        (
        ID INTEGER PRIMARY KEY NOT NULL,
        AUTHOR INTEGER,
        NUM_LIKES INTEGER,
        CONTENT TEXT,
        SOURCE TEXT,
        UPDATE_TIME INTEGER
        );
'''


def connect_db():
    conn = sqlite3.connect('/Users/king/Documents/WhatIHaveDone/wjl_eclipse_project/char-rnn-tensorflow/jiayuan/scrapy_crawler/scrapy_crawler/jokes')
    return conn


def close_db(conn):
    conn.close()


def md5str(str):
    return md5.new(str).hexdigest()


#def insert
if __name__ == '__main__':
    conn = sqlite3.connect('jokes')
    conn.execute(author_creator)
    #conn.execute('drop table JOKE;')
    conn.execute(joke_creator)
    #conn.execute('show tables;')
    conn.execute('select count(*) from QSBK_AUTHOR;')
    conn.close()
