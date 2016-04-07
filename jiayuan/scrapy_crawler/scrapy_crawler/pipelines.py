# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy_crawler.items import QiuShiBaiKeJokeItem, QiuShiBaiKeAuthorItem
from scrapy_crawler.util import *


class QiuShiBaiKePipeline(object):
    def open_spider(self, spider):
        self.conn = connect_db()
        self.num_jokes = 0

    def close_spider(self, spider):
        close_db(self.conn)

    def process_item(self, item, spider):
        if isinstance(item, QiuShiBaiKeAuthorItem):
            store_author(self.conn, item)
        elif isinstance(item, QiuShiBaiKeJokeItem):
            store_joke(self.conn, item)
        return item
