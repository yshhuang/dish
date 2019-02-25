import pymongo
import urllib.request
import json
import threading

import logging

logging.basicConfig(filename='logger.log', level=logging.INFO)

articleUrl_suffix = '?showmethod=native&keyfrom=wap&client=wap'
articleUrl_prefix = 'http://xue.youdao.com/sw/m/'

client = pymongo.MongoClient()
db = client['dish']
collection = db['youdao_dict']


def crawler_by_pid(pid):
    try:
        response = urllib.request.urlopen(articleUrl_prefix + str(pid) + articleUrl_suffix)
        result = response.read().decode('utf-8')
        article = json.loads(result)
        if article is None:
            return {}
        return article
    except:
        return crawler_by_pid(pid)


def insert_article(article):
    try:
        collection.insert_one(article).inserted_id
    except pymongo.errors.DuplicateKeyError:
        pass


def insert1():
    pid = 1600000
    print('thread %s is running...' % threading.current_thread().name)
    while pid > 1500000:
        article = crawler_by_pid(pid)
        if 'title' in article.keys():
            insert_article(article)
        pid = pid - 1
    print('thread %s is finished...' % threading.current_thread().name)


def insert2():
    pid = 1500000
    print('thread %s is running...' % threading.current_thread().name)
    while pid > 1400000:
        article = crawler_by_pid(pid)
        if 'title' in article.keys():
            insert_article(article)
        pid = pid - 1
    print('thread %s is finished...' % threading.current_thread().name)


def insert3():
    pid = 1400000
    print('thread %s is running...' % threading.current_thread().name)
    while pid > 1300000:
        article = crawler_by_pid(pid)
        if 'title' in article.keys():
            insert_article(article)
        pid = pid - 1
    print('thread %s is finished...' % threading.current_thread().name)


def insert4():
    pid = 1300000
    print('thread %s is running...' % threading.current_thread().name)
    while pid > 1200000:
        article = crawler_by_pid(pid)
        if 'title' in article.keys():
            insert_article(article)
        pid = pid - 1
    print('thread %s is finished...' % threading.current_thread().name)


def insert5():
    pid = 1200000
    print('thread %s is running...' % threading.current_thread().name)
    while pid > 1100000:
        article = crawler_by_pid(pid)
        if 'title' in article.keys():
            insert_article(article)
        pid = pid - 1
    print('thread %s is finished...' % threading.current_thread().name)


def insert6():
    pid = 1100000
    print('thread %s is running...' % threading.current_thread().name)
    while pid > 1000000:
        article = crawler_by_pid(pid)
        if 'title' in article.keys():
            insert_article(article)
        pid = pid - 1
    print('thread %s is finished...' % threading.current_thread().name)


def start_6_threads():
    t1 = threading.Thread(target=insert1, name='insert1')
    t2 = threading.Thread(target=insert2, name='insert2')
    t3 = threading.Thread(target=insert3, name='insert3')
    t4 = threading.Thread(target=insert4, name='insert4')
    t5 = threading.Thread(target=insert5, name='insert5')
    t6 = threading.Thread(target=insert6, name='insert6')
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()


def insert_latest_article(pid):
    empty = 0
    # pid = 1690000
    while empty < 100:
        # print(pid)
        logging.info(pid)
        article = crawler_by_pid(pid)
        if 'title' in article.keys():
            # print(article['title'])
            # logging.info(article['title'])
            insert_article(article)
            empty = 0
        else:
            empty = empty + 1
        pid = pid + 1


def get_max_pid():
    doc = collection.find().sort('pid', pymongo.DESCENDING).limit(1)
    return doc.next()['pid']


if __name__ == '__main__':
    # start_6_threads()

    max_pid = get_max_pid()
    insert_latest_article(max_pid)
