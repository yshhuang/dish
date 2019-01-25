import pymongo
import urllib.request
import json
import logging

logging.basicConfig(filename='logger.log', level=logging.INFO)

video_url_prefix = 'https://baobab.kaiyanapp.com/api/v1/video/'

client = pymongo.MongoClient()
db = client['dish']
collection = db['eyepetizer']


def crawler_by_id(id):
    url = video_url_prefix + str(id)
    try:
        response = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        result = urllib.request.urlopen(response).read().decode('utf-8')
        article = json.loads(result)
        if article is None:
            return {}
        return article
    except Exception as e:
        # print(e)
        return {}
        # return crawler_by_id(id)


def save_video(video):
    try:
        collection.insert_one(video).inserted_id
    except pymongo.errors.DuplicateKeyError:
        pass


def insert_latest_article(id):
    empty = 0
    # id = 1690000
    while empty < 100:
        # print(pid)
        logging.info(id)
        video = crawler_by_id(id)
        if 'title' in video.keys():
            # print(article['title'])
            logging.info(video['title'])
            save_video(video)
            empty = 0
        else:
            empty = empty + 1
        id = id + 1


def get_max_id():
    doc = collection.find().sort('id', pymongo.DESCENDING).limit(1)
    if doc.count() > 0:
        return doc.next()['id']
    else:
        return 0


if __name__ == '__main__':
    max_id = get_max_id()
    insert_latest_article(max_id)
