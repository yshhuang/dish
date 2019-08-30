import urllib.request as  req
import json
import sys
import os

post_list_url = "https://social.kkmh.com/v1/graph/label/posts/"
image_down_path = "/Volumes/develop/data/image/social-label/"

count = 0


def get_post_list(since):
    url = post_list_url + "&since=" + str(since)
    response = req.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    if data['code'] == 200:
        universalModels = data['data']['universalModels']
        for post in universalModels:
            download_post_img(post)
        # return data['data']
    else:
        return {}


def download_post_img(json):
    global count

    post = json.get('post')
    if post is None:
        return
    post_id = post['id']
    contents = post['content']
    # print(post['summary'])
    img_index = 0
    for content in contents:
        img_index += 1
        if content['type'] == 2:
            url = content['content']
            path = image_down_path + str(post_id) + '-' + str(img_index)
            if os.path.exists(path):
                continue
            req.urlretrieve(url, image_down_path + str(post_id) + '-' + str(img_index))
            count = count + 1
            print(count)
            if count == 100:
                sys.exit(1)


if __name__ == '__main__':
    # req.urlretrieve('http://f1.kkmh.com/e853fdf71561126b_1566881006.281875.png',
    #                 '/Volumes/develop/data/image/social-label/怦然心动/sss')
    argv = sys.argv
    post_list_url = post_list_url + argv[1] + "?filter=4&limit=10"
    image_down_path = image_down_path + argv[2] + "/"
    for i in range(0, 100):
        get_post_list(i)
        print("======" + str(i) + "=====")
