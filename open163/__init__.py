import pymongo
import urllib.request as req
import json
import os

movies_url_prefix = 'https://c.open.163.com/mob/'
movies_url_suffix = '/getMoviesForAndroid.do'

download_path = '/Volumes/develop/data/video/'

crawler_movies_set = {'ME2SKV6B0'}  # 待爬取视频plid集合
all_movies_set = set()  # 已爬取视频plid集合

client = pymongo.MongoClient()
db = client['dish']
collection = db['open163']


def get_movies(plid):
    try:
        response = req.urlopen(movies_url_prefix + plid + movies_url_suffix)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        if data['code'] == 200:
            return data['data']
        else:
            print(plid)
            return {}
    except:
        return get_movies(plid)


def insert_movies(movies):
    try:
        collection.insert_one(movies)
    except pymongo.errors.DuplicateKeyError:
        pass


def crawler_via_recommend():
    while len(crawler_movies_set) > 0:
        plid = crawler_movies_set.pop()
        movies = get_movies(plid)
        if len(movies) == 0:
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
        req.urlretrieve(video['mp4SdUrlOrign'], download_path + movies['title'] + '/' + video[
            'title'] + '.mp4')


if __name__ == '__main__':
    crawler_via_recommend()
    print('爬虫结束,共爬了%d个视频集合' % len(all_movies_set))
    # download_movies('M6SGF6VB4')
