import pymongo
import urllib.request as req
import json
import os, string
import time

movies_url_prefix = 'https://c.open.163.com/mob/'
movies_url_suffix = '/getMoviesForAndroid.do'

download_path = '/Volumes/develop/data/video/'

crawler_movies_set = {'ME2SKV6B0'}  # 待爬取视频plid集合
all_movies_set = set()  # 已爬取视频plid集合

client = pymongo.MongoClient()
db = client['dish']
collection = db['open163']

cher_arrary = list(string.ascii_uppercase) + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def get_movies(plid):
    try:
        response = req.urlopen(movies_url_prefix + plid + movies_url_suffix)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        if data['code'] == 200:
            return data['data']
        else:
            # print(plid)
            return {}
    except:
        print(plid)


def insert_movies(movies):
    try:
        collection.insert_one(movies)
    except pymongo.errors.DuplicateKeyError:
        pass


def crawler_via_recommend():
    while len(crawler_movies_set) > 0:
        plid = crawler_movies_set.pop()
        movies = get_movies(plid)
        if movies is None or len(movies) == 0:
            continue
        insert_movies(movies)
        all_movies_set.add(plid)
        all = len(all_movies_set)
        if all % 100 == 0:
            print('已导入%d部视频' % all)
        recommend_list = movies['recommendList']
        for recommend in recommend_list:
            recommend_plid = recommend['plid']
            if recommend_plid not in all_movies_set:
                crawler_movies_set.add(recommend_plid)


def download_movies(plid):
    movies = get_movies(plid)
    if not os.path.exists(download_path + movies['title']):
        os.mkdir(download_path + movies['title'])
    video_list = movies['videoList']
    for video in video_list:
        url = video['mp4SdUrl']
        if url == "":
            url = video['mp4SdUrlOrign']
        req.urlretrieve(url, download_path + movies['title'] + '/' + video[
            'title'] + '.mp4')


def add_plid(plid, cursor):
    if plid[cursor] == '9':
        plid = plid[:cursor]
        for index in range(9 - cursor):
            plid = plid + 'A'
        return add_plid(plid, cursor - 1)
    else:
        goal_char = plid[cursor]
        index = cher_arrary.index(goal_char)
        plid = plid[:cursor] + cher_arrary[index + 1] + plid[cursor + 1:]
        return plid


if __name__ == '__main__':
    # crawler_via_recommend()
    # print('爬虫结束,共爬了%d个视频集合' % len(all_movies_set))
    # plids = sys.argv
    # print(plids)
    # for i in range(1, len(sys.argv)):
    #     download_movies(sys.argv[i])
    plid = 'M6GLI5A07'
    while True:
        movies = get_movies(plid)
        if 'title' in movies.keys():
            localtime = time.asctime(time.localtime(time.time()))
            print(localtime, movies['title'])
            insert_movies(movies)
        plid = add_plid(plid, 8)
