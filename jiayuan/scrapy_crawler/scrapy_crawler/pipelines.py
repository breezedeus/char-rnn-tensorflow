# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy_crawler.items import QiuShiBaiKeJokeItem, QiuShiBaiKeAuthorItem
from scrapy_crawler.util import connect_db, close_db


class QiuShiBaiKePipeline(object):
    def open_spider(self, spider):
        self.conn = connect_db()

    def close_spider(self, spider):
        close_db(self.conn)

    def _store_author(self, author_item):
        one_row = author_item['id'], author_item['name'], author_item['status'], author_item['update_time']
        self.conn.execute('REPLACE INTO QSBK_AUTHOR VALUES (?,?,?,?)', one_row)
        self.conn.commit()

    def _store_joke(self, joke_item):
        one_row = joke_item['id'], joke_item['author'], joke_item['num_likes'], joke_item['content'], 'qiushibaike', joke_item['update_time']
        self.conn.execute('REPLACE INTO JOKE VALUES (?,?,?,?,?,?)', one_row)
        self.conn.commit()

    def process_item(self, item, spider):
        if isinstance(item, QiuShiBaiKeAuthorItem):
            self._store_author(item)
        elif isinstance(item, QiuShiBaiKeJokeItem):
            self._store_joke(item)
        return item
