import urllib.request as request
import urllib.parse as parse
import csv
import json

authkey = """
YpXFNw0+aCYtgKQS4woJ0BeLoxFBDy/FgT+u1KRk6g/I0eeBzdcEbROXEz6KvWqOFQPoxDvGZuF2IRbvYYmtHPTe+fFkJac0Om9
DTKl+wn0sS9doJPtpaYsE9WJeqnnk217eAYCDsZRYd+5a88tdaDi1bX/TWR7s9mZFjjLS6BbuT31/IWVwKdM3nfeEqjcS4IANipsdXOgh5s2oVF7
gHS0UIFnml1yK90r4/sxtS927VMV13gBNV+dmKeXOmolpYp4Dc/X2cO+yFOnxnfHYs4jIgiSNvVBkz/N8WFjSByKy6EwiE+fEeEEkbrvthn97MrR
dneb/w/5MOv7LwOwkQ7VRnFD8VtgrNCB5+vF7Ypqg+iQepJsah2BCmKGSbqv8IdiAGoliNanX+9CNmeNp1/FVzebnEog8eedsjtrO1HjzDPcBEqt
Mp5V1B29K8Ix8sxYqG1MhhJ1CYnOhRCtlDPdq/DjzQ+PST4sM4QLWpZ7pntDWhrcjti327D3fgwqFPge5ZhuYeTB6oco9GUsjnzFv+jeE8HTnTaU
BYh/V93v9TYum2p9cXfieIcwKM0K8rYgNKL/m8VpthDx6Nft9jmJz6v9wO57Nc10L/bZ74s+tRYtUcQWi5IGKcho/4fih0vKofrNatwSGvbcI099
T8YUCMMOYfDLyiPXodxo1762xwfPbEr941HK9FuBdh1akGGOY6MEdPFydem9CUq7Hh8hxySUjyd/sBsm763XktquFb8bmLGNcVothnnQXkTaXtaR
rvRhdc+TKixbu5E00FTG1/BLiy+C7SdMJ4bpUcFGr1Kdc6XziTidPmU/TK//xVUyoHptxHMi5+cmM+KvNxUpNCM/pKLK4btbz/7QLlik6xGj39vm
pUXoFbF+GLrwtpooty3Aemm/6Pzf1Mlmip4LUNc28+Ug5FYr7kiJi49I9rF8j5VENqxUpTAStwICuxoeabhektlO+rT5rQOksdIJBpSGre8KpSFe
h+v+J/lkv0udKJCi9hjrmIZ1GD6DV
"""
url = 'https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog'
params = {
    'authkey_ver': 1,
    'sign_type': 2,
    'auth_appid': 'webview_gacha',
    'init_type': 301,
    'gacha_id': 'd01c72488cc8b4450b535b4260577d0a58d4b9',
    'lang': 'zh-cn',
    'device_type': 'pc',
    'ext': {"loc": {"x": 1691.35009765625, "y": 285.5385437011719, "z": 385.6869201660156}, "platform": "WinST"},
    'region': 'region',
    'authkey': authkey,
    'game_biz': 'hk4e_cn',
    'gacha_type': 100,
    'end_id': 0,
    'page': 1,
    'size': 20
}

size = params.get('size')
rows=[]
while size == 20:
    encode_params = parse.urlencode(params)
    ret = request.urlopen(url + '?' + encode_params)
    ret_str = ret.read().decode('utf-8')
    rst_dict = json.loads(ret_str)

    if rst_dict['retcode'] != 0:
        print(rst_dict['message'])
        break
    data = rst_dict['data']
    list = data['list']
    for item in list:
        row=[item['uid'],item['gacha_type'],item['item_id'],item['count'],item['time'],item['name'],item['item_type'],
        item['rank_type'],item['id']]
        rows.append(row)
    params['page'] = params.get('page')+1
    params['end_id']=item['id']
    size = len(list)

headers = ['uid', 'gacha_type', 'item_id', 'count',
           'time', 'name', 'item_type', 'rank_type', 'id']


with open('new.csv', 'w')as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
