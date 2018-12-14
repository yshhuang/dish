import pymongo
import urllib.request
import json

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


if __name__ == '__main__':
    pid = 1677945
    while pid > 0:
        print(pid)
        article = crawler_by_pid(pid)
        if 'title' in article.keys():
            print(article['title'])
            insert_article(article)
        pid = pid - 1
