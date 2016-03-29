__author__ = 'king'
import sqlite3

author_creator = '''CREATE TABLE QSBK_AUTHOR
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT,
       STATUS            INT     NOT NULL,
       UPDATE_TIME         INT);'''

joke_creator = '''CREATE TABLE QSBK_JOKE
        (ID INT,
        BACK_ID INT,
        AUTHOR INT,
        NUM_LIKES INT,
        CONTENT TEXT,
        UPDATE_TIME INT
        );
'''

if __name__ == '__main__':
    conn = sqlite3.connect('jokes')
    conn.execute(author_creator)
    conn.execute(joke_creator)
    conn.execute('select count(*) from QSBK_AUTHOR')
    conn.close()
