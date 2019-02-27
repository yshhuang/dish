import pymongo
import urllib.request
import json

client = pymongo.MongoClient()
db = client['test']
collection = db['error']

if __name__ == '__main__':
    result = collection.find_one_and_update({'id': 2}, {'$set': {'id': 2, 'name': 'b', 'age': 320}})
    print(result)
    # collection.save({'id': 1, 'name': 'b'})
