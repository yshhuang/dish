import urllib
import urllib.request as req
import json
import os, string
import time

url_prefix = "https://yys.res.netease.com/pc/zt/20161108171335/data/"
download_path = "/Volumes/develop/data/image/yys/shishen/"


def download_skin(id, name, level):
    name = level + "/" + name
    if not os.path.exists(download_path + name):
        os.mkdir(download_path + name)
    try:
        before_awake_url = url_prefix + "shishen_big_beforeAwake/" + str(id) + ".png?v29"
        req.urlretrieve(before_awake_url, download_path + name + "/before-awake.png")
        after_awake_url = url_prefix + "shishen_big_afterAwake/" + str(id) + ".png?v29"
        req.urlretrieve(after_awake_url, download_path + name + "/after-awake.png")
    except urllib.error.HTTPError:
        print(id, name)
    i = 1;
    while i > 0:
        try:
            skin_url = url_prefix + "shishen_skin/" + str(id) + "-" + str(i) + ".png?v29"
            req.urlretrieve(skin_url, download_path + name + "/skin-" + str(i) + ".png")
        except urllib.error.HTTPError:
            return
        i = i + 1


def get_all_shishen():
    url = "https://yys.res.netease.com/pc/zt/20161108171335/js/app/all_shishen.json?v29"
    response = req.urlopen(url).read().decode('utf-8')
    data = json.loads(response)
    return data
    for data in datas:
        print(data["id"])


if __name__ == '__main__':
    shishens = get_all_shishen()
    print(len(shishens))
    for shishen in shishens:
        id = shishen["id"]
        name = shishen["name"]
        level = shishen["level"]
        download_skin(id, name, level)
