import json
import urllib.request as req

with open('/Volumes/develop/code-repository/python/dish/kuaikan/request.txt', 'r') as f:
    for line in f.readlines():
        requestParam = line.strip().split()[5][5:]
        jsonData = json.loads(requestParam)
        images = jsonData['images']
        imageStr = ','.join(images)
        postId = jsonData['postId']
        url = 'http://image.quickcan.com/image_service/append_cover?images=' + imageStr + "&postId=" + postId
        req.urlopen(url)
