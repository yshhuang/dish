from urllib import request
import re
from bs4 import BeautifulSoup
import sys

url = "https://blog.csdn.net/yshhuang"


def crawler_profile():
    profile = request.urlopen(url)
    bs = BeautifulSoup(profile, "lxml")
    articles = bs.select("div.article-list h4 > a")
    for article in articles:
        # title = article.get_text()
        link = article.get("href")
        # data = {
        #     '标题': title,
        #     '链接': link
        # }
        # print(data)
        if link != "https://blog.csdn.net/yoyo_liyy/article/details/82762601":
            request.urlopen(link)


if __name__ == '__main__':
    for i in range(100):
        crawler_profile()
        print(i)
