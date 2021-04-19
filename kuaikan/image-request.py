import json
import urllib.request as req

fi = open('/Volumes/develop/data/image.txt', 'a')
with open('/Volumes/develop/data/image-list.txt', 'r') as f:

    for line in f.readlines()[26520:]:
        jsonData = json.loads(line.strip().split()[7][8:])
        image = jsonData['spriteImageUrl']
        print(image)
        fi.write(image+"\n")
        # requestParam = line.strip().split()[5][5:]
        # jsonData = json.loads(requestParam)
        # images = jsonData['images']
        # imageStr = ','.join(images)
        # postId = jsonData['postId']
        # url = 'http://image.quickcan.com/image_service/append_cover?images=' + imageStr + "&postId=" + postId
        # req.urlopen(url)

fi.close()
