import urllib.request as  req
import json

post_list_url = "https://social.kkmh.com/v1/graph/label/posts/611742282583900208?filter=4&limit=10"
image_down_path = "/Volumes/develop/data/lolita/kuaikan/image/"


def get_post_list(since):
    try:
        url = post_list_url + "&since=" + str(since)
        print(url)
        response = req.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        if data['code'] == 200:
            universalModels = data['data']['universalModels']
            for post in universalModels:
                download_post_img(post)
            # return data['data']
        else:
            return {}
    except Exception as e:
        print(e.with_traceback())
        print(since)


def download_post_img(post):
    post = post['post']
    post_id = post['id']
    contents = post['content']
    # print(post['summary'])
    img_index = 0
    for content in contents:
        img_index += 1
        if content['type'] == 2:
            url = content['content']
            req.urlretrieve(url, image_down_path + str(post_id) + '-' + str(img_index))


if __name__ == '__main__':
    for i in range(49, 100):
        get_post_list(i)
        print(i)
        # print("===================================================")
