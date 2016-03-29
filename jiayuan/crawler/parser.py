__author__ = 'king'


import sys, os
import re
from bs4 import BeautifulSoup


class Joke(object):
    ANONYMOUS_AUTHOR_ID = 0

    def __init__(self, id, author, nickname, like_num, content):
        self.id = long(id)
        self.author = int(author)
        self.nickname = nickname
        self.like_sum = int(like_num)
        self.content = content

    def __cmp__(self, other):
        if self.id != other.id:
            return self.id - other.id

    def __str__(self):
        alls = (self.id, self.author, self.nickname, self.like_sum, self.content)
        return 'id = %d, author = %d, nickname = %s, like_sum = %d, content = %s' % alls


class QiuShiBaiKeParser(object):
    def __init__(self):
        pass

    def parse_joke(self, joke):
        author_nickname = joke.find('div', class_='author clearfix')
        try:
            author = author_nickname.select('a')[0]['href']
            author_pattern = re.compile('/users/([0-9]*)', re.S)
            author = re.findall(author_pattern, author)[0]
        except IndexError, e:
            author = str(Joke.ANONYMOUS_AUTHOR_ID)

        nickname = author_nickname.select('h2')[0].string.encode('utf-8')

        content_id = joke.find('div', class_='content')
        content = content_id.get_text().strip().encode('utf-8')
        id_pattern = re.compile('<!--([0-9]*)-->', re.S)
        id = re.findall(id_pattern, str(content_id))[0]

        like_num = joke.find('span', class_='stats-vote').select('i')[0].string

        joke = Joke(id=id, author=author, nickname=nickname, like_num=like_num, content=content)
        return joke

    def parse_file(self, file_name='../data/test.html'):
        soup = BeautifulSoup(open(file_name), 'html.parser')
        all_html_jokes = soup.find_all('div', class_="article block untagged mb15")
        all_jokes = []
        for html_joke in all_html_jokes:
            joke = self.parse_joke(html_joke)
            all_jokes.append(joke)
            #print(joke)
            #print('\n\n')
        return all_jokes


if __name__ == '__main__':
    #data_dir = sys.argv[1]
    data_dir = '../../data/qiushibaike/textnew'
    parser = QiuShiBaiKeParser()
    files = os.listdir(data_dir)
    files.sort()
    authors = set()
    jokes_from_anonymous = []
    for file_name in files:
        jokes = parser.parse_file(os.path.join(data_dir, file_name))
        authors.update([joke.author for joke in jokes])
        jokes_from_anonymous.append([joke for joke in jokes if joke.author == Joke.ANONYMOUS_AUTHOR_ID])
    print(len(authors))
    print(len(jokes_from_anonymous))
