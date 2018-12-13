import urllib.request
import json
import pymysql

listUrl = 'http://dict.youdao.com/infoline/style?client=mobile&apiversion=3.0&style=morning&order=desc' \
          '&keyfrom=mdict.7.8.2.android&model=MI_5s_Plus&mid=8.0.0&imei=99000828489816&vendor=xiaomi' \
          '&screen=1080x1920&ssid=kkmh&network=wifi&abtest=0'


def get_data(last_id=0, size='10'):
    url = listUrl
    if last_id is not None:
        url = url + '&lastId=' + last_id
    if size is not None:
        url = url + '&size=' + size
    response = urllib.request.urlopen(url)
    result = response.read().decode('utf-8')

    cards = json.loads(result)['cards']
    if len(cards) > 0:
        last_id = cards[-1]['id']
    return cards, last_id


def insert_into_mysql(data):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root1234',
        db='dish',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = """insert into youdao_dict(id, title, url, `type`, summary, media, keywords, style,
            channel_id, channel_name, audiourl, videourl, gif, image, start_time) 
            value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE title = title"""
            for line in data:
                cursor.execute(sql, (
                    line['id'], line['title'], line['url'], line['type'], line['summary'],
                    line['media'], json.dumps(line['keywords']), line['style'], line['channelId'],
                    line['channelName'], line['audiourl'], line['videourl'],
                    json.dumps(line['gif']),
                    json.dumps(line['image']), line['startTime']))
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()


if __name__ == '__main__':
    cards, lastId = get_data(None, '10')
    insert_into_mysql(cards)
    while len(cards) > 0:
        cards, lastId = get_data(lastId, '10')
        insert_into_mysql(cards)
    print('下载完成')
