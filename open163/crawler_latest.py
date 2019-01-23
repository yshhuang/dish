import pymongo
import urllib.request
import json
import logging

client = pymongo.MongoClient()
db = client['dish']
collection_subscribe = db['open163_subscribe']
collection_content = db['open163_content']
collection = db['open163']

subscribe_url_prefix = 'https://c.open.163.com/open/mob/subscribe/detail/info.do?subscribeId='
content_url_prefix = 'https://c.open.163.com/open/mob/subscribe/detail/list.do' \
                     '?rtypes=2%2C3%2C4%2C5%2C6%2C8%2C9%2C10%2C11%2C12'
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


def update_subscribe(subscribe):
    try:
        collection_subscribe.update_one({'subscribeId': subscribe['subscribeId']},
                                        {"$set": subscribe}, True)
    except pymongo.errors.DuplicateKeyError:
        pass


def get_max_subscribeId():
    doc = collection_subscribe.find().sort('subscribeId', pymongo.DESCENDING).limit(1)
    return doc.next()['subscribeId']


def find_by_subscribeId(subscribeId):
    doc = collection_subscribe.find_one({'subscribeId': subscribeId})
    return doc


def crawler_latest_subscribe(subscribeId):
    empty = 0
    while empty < 100:
        subscribe_before = find_by_subscribeId(subscribeId)
        subscribe = crawler_subscribe(subscribeId)
        if 'subscribeName' in subscribe.keys():
            print(subscribe['subscribeName'])
            if subscribe_before is None or 'subscribeArticleCount' not in subscribe_before.keys():
                size = subscribe['subscribeArticleCount']
            else:
                size = subscribe['subscribeArticleCount'] - subscribe_before[
                    'subscribeArticleCount']
            print(size)
            update_subscribe(subscribe)
            if size > 0:
                crawler_content(subscribeId, size)
            empty = 0
        else:
            empty = empty + 1
        subscribeId = subscribeId + 1


def crawler_content(subscribeId, size):
    try:
        url = content_url_prefix + '&subscribeId=' + str(subscribeId) + '&pagesize=' + str(size)
        response = urllib.request.urlopen(url)
        result = response.read().decode('utf-8')
        content = json.loads(result)
        if content is None or 'data' not in content.keys():
            return {}
        else:
            insert_contents(content['data'])
    except:
        return {}


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


if __name__ == '__main__':
    crawler_latest_subscribe(1)
