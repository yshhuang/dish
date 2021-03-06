import pymongo
import urllib.request
import json
import logging

logging.basicConfig(filename='logger.log', level=logging.INFO)

client = pymongo.MongoClient()
db = client['dish']
collection_subscribe = db['open163_subscribe']
collection_content = db['open163_content']
collection = db['open163_movie']

subscribe_url_prefix = 'https://c.open.163.com/open/mob/subscribe/detail/info.do?subscribeId='
content_url_prefix = 'https://c.open.163.com/open/mob/subscribe/detail/list.do' \
                     '?rtypes=2%2C3%2C4%2C5%2C6%2C8%2C9%2C10%2C11%2C12&pagesize=10'
movies_url_prefix = 'https://c.open.163.com/mob/'
movies_url_suffix = '/getMoviesForAndroid.do'

all_plid_set = set()


def crawler_subscribe(subscribeId):
    try:
        response = urllib.request.urlopen(subscribe_url_prefix + str(subscribeId))
        result = response.read().decode('utf-8')
        subscribe = json.loads(result)
        if subscribe is None or 'data' not in subscribe.keys():
            return {}
        return subscribe['data']
    except:
        return crawler_subscribe(subscribeId)


def insert_subscribe(subscribe):
    try:
        collection_subscribe.insert_one(subscribe)
    except pymongo.errors.DuplicateKeyError:
        pass


def insert_contents(contents):
    if len(contents) == 0:
        return
    else:
        try:
            collection_content.insert_many(contents)
        except pymongo.errors.BulkWriteError:
            pass
    for content in contents:
        if content['plid'] not in all_plid_set:
            insert_movies(content['plid'])
            all_plid_set.add(content['plid'])


def insert_movies(plid):
    try:
        response = urllib.request.urlopen(movies_url_prefix + plid + movies_url_suffix)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        if data['code'] == 200:
            try:
                collection.insert_one(data['data'])
            except pymongo.errors.DuplicateKeyError:
                pass
    except:
        print(plid)


def crawler_all_subscribe():
    empty = 0
    subscribeId = 1
    while empty < 100:
        subscribe = crawler_subscribe(subscribeId)
        if 'subscribeName' in subscribe.keys():
            print(subscribe['subscribeName'])
            insert_subscribe(subscribe)
            crawler_content(subscribeId)
            empty = 0
        else:
            empty = empty + 1
        subscribeId = subscribeId + 1


def crawler_content(subscribeId):
    content = []
    cursor = ''
    result = crawler_content_page(subscribeId, cursor)
    while 'data' in result.keys() and 'cursor' in result.keys():
        content = content + result['data']
        cursor = result['cursor']
        result = crawler_content_page(subscribeId, cursor)
    if 'data' in result.keys():
        content = content + result['data']
    print(len(content))
    insert_contents(content)


def crawler_content_page(subscribeId, cursor=''):
    try:
        # print(subscribe_url_prefix)
        url = content_url_prefix + '&subscribeId=' + str(
            subscribeId) + '&cursor=' + cursor
        response = urllib.request.urlopen(url)
        result = response.read().decode('utf-8')
        content = json.loads(result)
        if content is None or 'data' not in content.keys():
            return {}
        return content
    except:
        print(subscribeId)
        return crawler_content_page(subscribeId, cursor='')


if __name__ == '__main__':
    crawler_all_subscribe()
    # crawler_content(19)
