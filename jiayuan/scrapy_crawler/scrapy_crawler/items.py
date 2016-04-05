# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


ANONYMOUS_AUTHOR_ID = 0

class QiuShiBaiKeJokeItem(scrapy.Item):
    id = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    num_likes = scrapy.Field()
    update_time = scrapy.Field()


class QiuShiBaiKeAuthorItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
    update_time = scrapy.Field()
