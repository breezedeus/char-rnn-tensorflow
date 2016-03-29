__author__ = 'king'

import re
import unittest
from bs4 import BeautifulSoup


class Joke(object):
    def __init__(self, id, author, nickname, like_num, content):
        self.id = long(id)
        self.author = int(author)
        self.nickname = nickname
        self.like_sum = int(like_num)
        self.content = content

    def __str__(self):
        alls = (self.id, self.author, self.nickname, self.like_sum, self.content)
        return 'id = %d, author = %d, nickname = %s, like_sum = %d, content = %s' % alls


class TestBeautifulSoup(unittest.TestCase):
    def parse_joke(self, joke):
        author_nickname = joke.find('div', class_='author clearfix')
        try:
            author = author_nickname.select('a')[0]['href']
            author_pattern = re.compile('/users/([0-9]*)', re.S)
            author = re.findall(author_pattern, author)[0]
        except IndexError, e:
            author = '-1'

        nickname = author_nickname.select('h2')[0].string.encode('utf-8')

        content_id = joke.find('div', class_='content')
        content = content_id.get_text().strip().encode('utf-8')
        id_pattern = re.compile('<!--([0-9]*)-->', re.S)
        id = re.findall(id_pattern, str(content_id))[0]

        like_num = joke.find('span', class_='stats-vote').select('i')[0].string

        joke = Joke(id=id, author=author, nickname=nickname, like_num=like_num, content=content)
        return joke

    def test_something(self):
        self.file_name = '../data/test.html'
        soup = BeautifulSoup(open(self.file_name), 'html.parser')
        all_jokes = soup.find_all('div', class_="article block untagged mb15")
        for joke in all_jokes:
            new_joke = self.parse_joke(joke)
            print(new_joke)
            print('\n\n')



