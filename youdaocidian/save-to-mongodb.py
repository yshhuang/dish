import pymongo
import urllib.request
import json
import threading

articleUrl_suffix = '?showmethod=native&keyfrom=wap&client=wap'
articleUrl_prefix = 'http://xue.youdao.com/sw/m/'

client = pymongo.MongoClient()
db = client['dish']
collection = db['youdao_dict']
error_collection = db['error']


def crawler_by_pid(pid):
    response = urllib.request.urlopen(articleUrl_prefix + str(pid) + articleUrl_suffix)

    # print(result.substring(120, 130))
    try:
        result = response.read().decode('utf-8')
        article = json.loads(result)
        return article
    # except Exception as e:
    #     error_collection.insert_one({'project': '有道词典', 'method': 'crawler_by_pid',
    #                                  'params': pid})
    #     print(article)
    except:
        return {}


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


if __name__ == '__main__':
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

    # pid = 1683800
    # while pid > 0:
    #     print(pid)
    #     article = crawler_by_pid(pid)
    #     if 'title' in article.keys():
    #         print(article['title'])
    #         insert_article(article)
    #     pid = pid - 1
