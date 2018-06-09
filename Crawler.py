import re
import time
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Crawler:

    numberOfArticles = 100

    @staticmethod
    def readParagraphs(url):
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                html = response.read()
        except Exception:
            return ''
        soup = BeautifulSoup(html, 'html.parser')
        text = ''
        for p in soup.find_all('p'):
            text += p.get_text()
        return text

    def crawl(self, tag):
        browser = webdriver.Firefox(r'/home/kinga/Programs/selenium_driver/geckodriver-v0.20.1-linux64')

        browser.get('https://www.wykop.pl/tag/znaleziska/' + tag + '/najlepsze')
        time.sleep(1)
        elem = browser.find_element_by_tag_name("body")
        no_of_pagedowns = 200

        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            no_of_pagedowns -= 1

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        articles = set()
        for link in soup.find_all('a', title=re.compile('Otwórz źródło znaleziska'), href=True):
            if not link['href'].startswith('http://www.youtube.com') and not link['href'].startswith('http://youtu.be')\
            and not link['href'].startswith('https://www.youtube.com') and not link['href'].startswith('https://youtu.be'):
                articles.add(link['href'])

        text = ''
        articlesList = list(articles)
        for article in articlesList[:self.numberOfArticles]:
            print('Loading data from:', article)
            text += self.readParagraphs(article)
        browser.close()
        return text


def readTags():
    with open('tags.txt') as f:
        tags = f.readline()
    tags = tags.split()
    return tags


if __name__ == '__main__':
    crawler = Crawler()
    tags = readTags()

    for tag in tags:
        print('Downloading data for tag:', tag)
        text = crawler.crawl(tag)
        file = open('texts/' + tag + '.txt', 'a')
        file.write(text)

    print('Finished')