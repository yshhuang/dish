import urllib.request
import re
from lxml import etree


# 封装获取网页所有信息的函数
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html


# 封装获取满足正则表达式的图片地址
def getImg(content):
    xml = etree.HTML(content)
    # print(content)
    datas = xml.xpath('//*[@id="__layout"]/div/div/div[2]/div[1]/div[4]/img/@src')
    print(datas)
    return datas


if __name__ == "__main__":
    html = getHtml("https://www.kuaikanmanhua.com/web/comic/129558/")
    # print(html)
    i = 0
    for imgurl in getImg(html):
        urllib.request.urlretrieve(imgurl, "/Volumes/develop/data/image/kuaikan-web/%s.jpg" % i)
        i += 1
