# -*- coding: utf8 -*-
__author__ = 'king'

from datetime import datetime
import re, time, os
import scrapy

from scrapy_crawler.items import QiuShiBaiKeJokeItem, QiuShiBaiKeAuthorItem, ANONYMOUS_AUTHOR_ID
from scrapy_crawler.settings import STORAGE_DIR
from scrapy_crawler.util import connect_db, close_db

class QiuShiBaiKeSpider(scrapy.Spider):
    name = 'qiushibaike'
    allowed_domains = ['qiushibaike.com']
    start_urls = [
        "http://www.qiushibaike.com/textnew/",
        "http://www.qiushibaike.com/history/",
    ]

    def __init__(self, *args, **kwargs):
        super(QiuShiBaiKeSpider, self).__init__(*args, **kwargs)
        self.conn = connect_db()

    def close(self, reason):
        close_db(self.conn)

    def _author_already_crawled(self, author_id):
        cursor = self.conn.execute('select status from QSBK_AUTHOR where id = %d' % author_id)
        for row in cursor:
            status = row[0]
            if status is not None and status == 1:
                return False
            else:
                return True

    def _set_author_status(self, author_id, status=1):
        self.conn.execute('update QSBK_AUTHOR set status = %d where id = %d' % (status, author_id))
        self.conn.commit()

    def _joke_already_existed(self, joke_id):
        cursor = self.conn.execute('select author from JOKE where id = %d' % joke_id)
        for row in cursor:
            status = row[0]
            if status is not None:
                return True
            else:
                return False

    def parse(self, response):
        self.logger.info('Parsing url %s ...', response.url)
        def store():
            data_dir = os.path.join(STORAGE_DIR, 'qiushibaike')
            layout = 'textnew'
            output_dir = os.path.join(data_dir, layout)
            output_dir = os.path.join(output_dir, time.strftime('%Y.%m.%d', time.localtime(time.time())))
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            file_name = str(int(time.time())) + '.html'
            file_name = os.path.join(output_dir, file_name)
            with open(file_name, 'w') as f:
                f.write(response.body)
        store()

        article_id_pattern = re.compile('.*?_([0-9].*)$', re.S)
        author_pattern = re.compile('/users/([0-9]*)', re.S)
        for joke in response.xpath('//div[@class="article block untagged mb15"]'):
            article_id = joke.xpath('@id').extract_first()
            article_id = int(re.findall(article_id_pattern, article_id)[0].strip())
            if self._joke_already_existed(article_id):
                return
            author_link = joke.xpath('div[@class="author clearfix"]/a/@href')
            author_link = author_link.extract_first()
            if author_link is not None:
                author_id = int(re.findall(author_pattern, author_link)[0].strip())
                if not self._author_already_crawled(author_id=author_id):
                    author_name = joke.xpath('div[@class="author clearfix"]/a/h2/text()').extract_first().strip()
                    author_item = QiuShiBaiKeAuthorItem()
                    author_item['id'] = author_id
                    author_item['name'] = author_name
                    author_item['status'] = 0
                    author_item['update_time'] = int(time.time())
                    yield author_item
                    # parse author page
                    url = response.urljoin(author_link)
                    #print(url)
                    yield scrapy.Request(url, callback=self.parse_authorpage)
            else:
                author_id = ANONYMOUS_AUTHOR_ID
            has_image = joke.xpath('div[@class="thumb"]/a[contains(@href, "article")]/img/@src').extract_first()
            if has_image is not None:
                continue
            content = ''.join(joke.xpath('div[@class="content"]/text()').extract()).strip()
            num_likes = int(joke.xpath('div/span[@class="stats-vote"]/i/text()').extract_first().strip())
            update_time = int(time.time())  # datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print(article_id, author_id, content, num_likes, update_time)

            joke_item = QiuShiBaiKeJokeItem()
            joke_item['id'] = article_id
            joke_item['author'] = author_id
            joke_item['content'] = content
            joke_item['num_likes'] = num_likes
            joke_item['update_time'] = update_time
            yield joke_item

        def get_nextpage():
            for link in response.xpath('//ul[@class="pagination"]/li'):
                nextpage_link = link.xpath('a/span[@class="next"]').extract_first()
                if nextpage_link is not None:
                    nextpage_link = link.xpath('a/@href').extract_first()
                    url = response.urljoin(nextpage_link)
                    #print(url)
                    return scrapy.Request(url, callback=self.parse)
        yield get_nextpage()


    def parse_authorpage(self, response):
        self.logger.info('Parsing url %s ...', response.url)
        url_segs = response.url.split("/")
        def get_author_id():
            length = len(url_segs)
            for i, seg in enumerate(url_segs):
                if seg == 'users' and i+1 <= length:
                    return int(url_segs[i+1])
        author_id = get_author_id()

        def store():
            data_dir = os.path.join(STORAGE_DIR, 'qiushibaike')
            layout = 'authorpage'
            output_dir = os.path.join(data_dir, layout)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            page = 1
            if url_segs[-2] == 'page':
                page = int(url_segs[-1])
            file_name = '%d_%d.html' % (author_id, page)
            file_name = os.path.join(output_dir, file_name)
            with open(file_name, 'w') as f:
                f.write(response.body)
        store()

        article_id_pattern = re.compile('/article/([0-9]*)$', re.S)
        numlikes_pattern = re.compile('([0-9]*).*?', re.S)
        for joke in response.xpath('//div[@class="qiushi_body article clearfix"]/div[@class="content clearfix"]'):
            article_id = joke.xpath('a/@href').extract_first()
            article_id = int(re.findall(article_id_pattern, article_id)[0].strip())
            has_image = joke.xpath('a/img[@class="pic"]/@src').extract_first()
            if has_image is not None:
                continue
            content = ''.join(joke.xpath('a/text()').extract()).strip()
            num_likes = joke.xpath('div/span[@class="up"]/text()').extract_first().strip()
            num_likes = int(re.findall(numlikes_pattern, num_likes)[0].strip())
            update_time = joke.xpath('div/span[@class="time"]/text()').extract_first().strip()
            #print(article_id, author_id, content, num_likes, update_time)

            joke_item = QiuShiBaiKeJokeItem()
            joke_item['id'] = article_id
            joke_item['author'] = author_id
            joke_item['content'] = content
            joke_item['num_likes'] = num_likes
            joke_item['update_time'] = int(time.mktime(time.strptime(update_time, '%Y-%m-%d')))
            yield joke_item

        def get_nextpage():
            nextpage_link = response.xpath('//a[@class="next"]/@href').extract_first()
            if nextpage_link is not None:
                #print('nextpage_link=' + nextpage_link)
                url = response.urljoin(nextpage_link)
                #print(url)
                return scrapy.Request(url, callback=self.parse_authorpage)
            return None
        nextpage_request = get_nextpage()
        if nextpage_request is not None:
            yield nextpage_request
        else:
            self._set_author_status(author_id=author_id, status=1)


    def parse_xxx(self, response):
        self.parse_mainpage(response)
        return
        for article in response.xpath("//div[contains(@class, 'article')]"):
             item = QiuShiItem()
             author_sel =  article.xpath('div[contains(@class, "author")]/a')
             item['header'] = author_sel.xpath('img/@src').extract()          # 用户头像
             item['author'] = "".join(author_sel.xpath('h2/text()').extract()).strip()   # 用户名称
             content_sel = article.xpath('div[@class="content"]')
             item['content'] = content_sel.xpath('text()').extract()        # 内容
             item['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # content_sel.xpath('@title').extract()     # 内容创建日期
             item['thumb'] = article.xpath("div[contains(@class, 'thumb')]/a/img/@src").extract()  # 内容附件图片

             yield item

        # 得到下一页链接地址
        next_href = response.xpath("//ul[contains(@class, 'pagination')]/li/a/span[contains(@class, 'next')]/../@href").extract_first()
        url = "http://www.qiushibaike.com" + next_href.strip()
        current_pageNo = response.xpath('//ul[contains(@class, "pagination")]/li/span[contains(@class, "current")]/text()').extract()
        current = current_pageNo[0].strip()
        # 只爬取首页面的35页内容
        if(int(current)!=35):
            yield scrapy.Request(url, callback=self.parse)

