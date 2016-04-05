__author__ = 'king'
import unittest
from util import connect_db, close_db


class TestSqlite3(unittest.TestCase):
    def test_select(self):
        conn = connect_db()
        id = 0
        cursor = conn.execute('select status from QSBK_AUTHOR where id = %d' % id)
        print(cursor)
        #print(cursor.arraysize)
        for row in cursor:
            status = row[0]
            assert status is None
            print(status)
        close_db(conn)
