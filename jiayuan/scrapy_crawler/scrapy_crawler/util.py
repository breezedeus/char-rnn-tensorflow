__author__ = 'king'
import sqlite3
import md5

AUTHOR_TABLE = 'QSBK_AUTHOR'
JOKE_TABLE = 'JOKE'

author_creator = 'CREATE TABLE %s \
       (ID INT PRIMARY KEY     NOT NULL, \
       NAME           TEXT, \
       STATUS            INT     NOT NULL, \
       UPDATE_TIME         INT);' % AUTHOR_TABLE

joke_creator = 'CREATE TABLE %s \
        ( \
        ID INTEGER PRIMARY KEY NOT NULL, \
        AUTHOR INTEGER, \
        NUM_LIKES INTEGER, \
        CONTENT TEXT, \
        SOURCE TEXT, \
        UPDATE_TIME INTEGER \
        );' % JOKE_TABLE

def connect_db():
    conn = sqlite3.connect('/Users/king/Documents/WhatIHaveDone/wjl_eclipse_project/char-rnn-tensorflow/jiayuan/scrapy_crawler/scrapy_crawler/jokes')
    #conn = sqlite3.connect('/root/softwares/char-rnn-tensorflow/jiayuan/scrapy_crawler/jokes')
    return conn


def close_db(conn):
    conn.close()


def record_already_existed(conn, record_id, table_name):
    cursor = conn.execute('select * from %s where id = %d' % (table_name, record_id))
    for row in cursor:
        if row[0] is not None:
            return True
        else:
            return False


def joke_already_existed(conn, joke_id):
    return record_already_existed(conn=conn, record_id=joke_id, table_name=JOKE_TABLE)


def author_already_existed(conn, author_id):
    return record_already_existed(conn=conn, record_id=author_id, table_name=AUTHOR_TABLE)


def author_already_crawled(conn, author_id):
    cursor = conn.execute('select status from %s where id = %d' % (AUTHOR_TABLE, author_id))
    for row in cursor:
        status = row[0]
        if status is not None and status == 1:
            return False
        else:
            return True


def set_author_status(conn, author_id, status=1):
    conn.execute('update %s set status = %d where id = %d' % (AUTHOR_TABLE, status, author_id))
    conn.commit()


NUM_NEW_AUTHORS = 0
def store_author(conn, author_item):
    global NUM_NEW_AUTHORS
    if author_already_existed(conn, author_item['id']):
        return
    one_row = author_item['id'], author_item['name'], author_item['status'], author_item['update_time']
    conn.execute('REPLACE INTO %s VALUES (?,?,?,?)' % AUTHOR_TABLE, one_row)
    conn.commit()
    NUM_NEW_AUTHORS += 1
    print('num_authors = %d, with author_id = %d' % (NUM_NEW_AUTHORS, author_item['id']))


NUM_NEW_JOKES = 0
def store_joke(conn, joke_item):
    global NUM_NEW_JOKES
    if joke_already_existed(conn, joke_item['id']):
        return
    one_row = joke_item['id'], joke_item['author'], joke_item['num_likes'], joke_item['content'], 'qiushibaike', joke_item['update_time']
    conn.execute('REPLACE INTO %s VALUES (?,?,?,?,?,?)' % JOKE_TABLE, one_row)
    conn.commit()
    NUM_NEW_JOKES += 1
    print('num_jokes = %d, with joke_id = %d, author_id = %d' % (NUM_NEW_JOKES, joke_item['id'], joke_item['author']))


def md5str(str):
    return md5.new(str).hexdigest()


#def insert
if __name__ == '__main__':
    conn = connect_db()
    conn.execute(author_creator)
    #conn.execute('drop table JOKE;')
    conn.execute(joke_creator)
    #conn.execute('show tables;')
    conn.execute('select count(*) from QSBK_AUTHOR;')
    close_db(conn)
