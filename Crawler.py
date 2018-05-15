import re
import urllib.request
from bs4 import BeautifulSoup


class Crawler:
    @staticmethod
    def read_paragraphs(url):
        try:
            with urllib.request.urlopen(url) as response:
                html = response.read()
        except Exception:
            return ''
        soup = BeautifulSoup(html, 'html.parser')
        text = ''
        for p in soup.find_all('p'):
            text += p.get_text()
        return text

    def crawl(self, tag):
        with urllib.request.urlopen('https://www.wykop.pl/tag/znaleziska/' + tag) as response:
            html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        articles = set()
        for link in soup.find_all('a', title=re.compile('Otwórz źródło znaleziska'), href=True):
            if not link['href'].startswith('http://www.youtube.com'):
                articles.add(link['href'])

        text = ''
        for article in articles:
            print('\n\nLoading data from:', article, '\n')
            text += self.read_paragraphs(article)
        return text


if __name__ == '__main__':
    crawler = Crawler()
    tags = ['politechnika', 'uniwersytet', 'motoryzacja', 'sport', 'literatura', 'film', 'uroda', 'polityka', 'nauka', 'biznes']
    for tag in tags:
        text = crawler.crawl(tag)
        file = open(tag + '.txt', 'a')
        file.write(text)