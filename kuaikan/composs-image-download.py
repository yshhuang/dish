# encoding:utf-8
"""
@Time    : 2020-03-05 18:10
@Author  : yshhuang@foxmail.com
@File    : composs-image-download.py
@Software: PyCharm
"""
import urllib.request as req

url = 'http://f1.kkmh.com/'
qiniupath = "/Volumes/develop/data/image/kuaikan-web/qiniu/"
guepath = "/Volumes/develop/data/image/kuaikan-web/gue/"


def download_qiniu():
    with open('/Volumes/develop/code-repository/python/dish/kuaikan/qiniu.txt', 'r') as f:
        for line in f.readlines():
            try:
                info = line.strip().split()[4].split(',')
                origin = info[1][3:]
                compress = info[2][5:]
                print(origin)
                req.urlretrieve(url + origin, qiniupath + origin + ".jpg")
                req.urlretrieve(url + compress, qiniupath + compress + ".jpg")
            except req.HTTPError:
                continue


def download_gue():
    with open('/Volumes/develop/code-repository/python/dish/kuaikan/gue.txt', 'r') as f:
        for line in f.readlines():
            try:
                info = line.strip().split()[10]
                origin = info[5:len(info) - 1]
                compress = origin + "-compress-gue"
                print(origin)
                req.urlretrieve(url + origin, guepath + origin + ".jpg")
                req.urlretrieve(url + compress, guepath + compress + ".jpg")
            except req.HTTPError:
                continue


# 七牛压缩成功,原图:ebd35a5921d3155f_1583402373544281262158-watermark,压缩后图:ebd35a5921d3155f_1583402373544281262158-watermark-compress,原图大小:220611,压缩后大小:129832

if __name__ == '__main__':
    # download_gue()
    download_qiniu()