import urllib.request as req
import json
import sys
import os
import pymysql

post_list_url = "https://social.kkmh.com/v1/graph/label/posts/"
image_down_path = "/Volumes/develop/data/image/social-label/"

count = 0

# connection = pymysql.connect(host='localhost',
#                              port=3306,
#                              user='root',
#                              password='root1234',
#                              db='dish',
#                              charset='utf8')
labelId = ""


def get_post_list(since):
    url = post_list_url + "&since=" + str(since)
    response = req.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    if data['code'] == 200:
        universalModels = data['data']['universalModels']
        for post in universalModels:
            download_origin_img(post)
            # save_image(post)
        # return data['data']
    else:
        return {}


# def save_image(json):
#     global count
#
#     post = json.get('post')
#     if post is None:
#         return
#     post_id = post['id']
#     contents = post['content']
#     # print(post['summary'])
#     img_index = 0
#     for content in contents:
#         img_index += 1
#         if content['type'] == 2:
#             url = content['content']
#             path = image_down_path + str(post_id) + '-' + str(img_index)
#             if os.path.exists(path):
#                 continue
#             cursor = connection.cursor()
#             effect_row = cursor.execute(
#                 "INSERT INTO `image_similarity_url` (`url`, `label_ids`,`post_id`) VALUES (%s, "
#                 "%s,%s) ON DUPLICATE KEY ""UPDATE label_ids=JSON_MERGE_PATCH(label_ids,%s)",
#                 (url, "{\"" + labelId + "\":1}", post_id, "{\"" + labelId + "\":1}"))
#             connection.commit()
#
#             if effect_row == 1:
#                 count = count + 1
#                 print(count)
#             if count == 10000:
#                 sys.exit(1)


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
            if count == 10000:
                sys.exit(1)


def download_origin_img(json):
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
            origin = url
            if '-watermark' in url:
                origin = url[:url.find('-watermark')]
            path = image_down_path + origin[origin.rfind("/") + 1:]
            if os.path.exists(path):
                continue
            try:
                req.urlretrieve(origin, image_down_path + origin[origin.rfind("/") + 1:])
            except Exception as e:
                try:
                    origin_jpg = origin + ".jpg"
                    req.urlretrieve(origin_jpg,
                                    image_down_path + origin_jpg[origin_jpg.rfind("/") + 1:])
                except Exception as e:
                    try:
                        origin_png = origin + ".png"
                        req.urlretrieve(origin_png,
                                        image_down_path + origin_png[origin_png.rfind("/") + 1:])
                    except Exception as e:
                        print(e)
                        print(url)
            count = count + 1
            if count % 100 == 0:
                print(count)


if __name__ == '__main__':
    # req.urlretrieve('http://f1.kkmh.com/e853fdf71561126b_1566881006.281875.png',
    #                 '/Volumes/develop/data/image/social-label/怦然心动/sss')
    argv = sys.argv
    post_list_url = post_list_url + argv[1] + "?filter=4&limit=10"
    image_down_path = image_down_path + argv[2] + "/"
    labelId = argv[1]
    for i in range(0, 1000):
        get_post_list(i)
        print("======" + str(i) + "=====")
    # url = "https://pum-f1.kkmh.com/c3640cb50c603b48ed39180ca4a8aa3a_1585441408276-watermark-compress"
    # url = url[:url.find('-watermark')]
    # print(url[url.rfind("/")+1:])
