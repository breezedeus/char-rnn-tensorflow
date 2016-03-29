# -*- coding:utf-8 -*-
__author__ = 'king'
import urllib2
import time
import codecs
import os, sys, math


#糗事百科爬虫类
class QiuShiBaiKeCrawler:
    #初始化方法，定义一些变量
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.page_idx = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        #初始化headers
        self.headers = {'User-Agent': self.user_agent}
        #存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        #存放程序是否继续运行的变量
        self.enable = False

        self.confs = {'textnew': {'url': 'http://www.qiushibaike.com/textnew/page/', 'num_pages': 35, 'output_dir': 'textnew'}}

    def _get_url(self, layout):
        return self.confs[layout]['url']

    def _get_num_pages(self, layout):
        return self.confs[layout]['num_pages']

    def _get_output_dir(self, layout):
        return self.confs[layout]['output_dir']

    def crawl_page(self, page_idx, layout):
        output_dir = os.path.join(self.data_dir, self._get_output_dir(layout=layout))
        output_dir = os.path.join(output_dir, time.strftime('%Y.%m.%d', time.localtime(time.time())))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        file_name = str(int(time.time())) + '.html'
        file_name = os.path.join(output_dir, file_name)
        try:
            url = self._get_url(layout) + str(page_idx)
            #构建请求的request
            request = urllib2.Request(url, headers=self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转化为UTF-8编码
            page_content = response.read().decode('utf-8')

            with codecs.open(file_name, 'w', 'utf-8') as f:
                f.write(page_content)
                print('Done for file ' + file_name)
            return page_content

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接糗事百科失败,错误原因", e.reason
                return None

    def crawl(self, layout='textnew', mode='full'):
        total_num_pages = self._get_num_pages(layout)
        if mode != 'full':
            total_num_pages = 1
        for page_idx in range(1, total_num_pages + 1):
            self.crawl_page(page_idx=page_idx, layout=layout)
            time.sleep(10)


if __name__ == '__main__':
    output_dir = '../../data/qiushibaike'
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    spider = QiuShiBaiKeCrawler(output_dir)
    #mode = 'full'
    #spider.crawle(mode=mode)
    while True:
        try:
            spider.crawl(mode='update')
        except Exception, e:
            print('Warning: ' + e.message)
        time.sleep(300)
