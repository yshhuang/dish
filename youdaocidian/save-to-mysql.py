import urllib.request
import json
import pymysql

cardsUrl = 'http://dict.youdao.com/infoline/style?client=mobile&apiversion=3.0&style=morning&order=desc' \
           '&keyfrom=mdict.7.8.2.android&model=MI_5s_Plus&mid=8.0.0&imei=99000828489816&vendor=xiaomi' \
           '&screen=1080x1920&ssid=kkmh&network=wifi&abtest=0'
articleUrl_suffix = '?showmethod=native&keyfrom=wap&client=wap'
articleUrl_prefix = 'http://xue.youdao.com/sw/m/'
cards = []
articles = []


def get_cards(last_id=0, size='10'):
    url = cardsUrl
    if last_id is not None:
        url = url + '&lastId=' + last_id
    if size is not None:
        url = url + '&size=' + size
    response = urllib.request.urlopen(url)
    result = response.read().decode('utf-8')

    card_list = json.loads(result)['cards']
    if len(card_list) > 0:
        last_id = card_list[-1]['id']
    return card_list, last_id


def get_article(url):
    response = urllib.request.urlopen(url + articleUrl_suffix)
    result = response.read().decode('utf-8')
    article = json.loads(result)
    return article


def insert_into_mysql():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root1234',
        db='dish',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = connection.cursor()

    global articles
    for card in cards:
        try:
            article = get_article(card['url'])
            sql = """insert into youdao_dict(pid, title, card_id, card_title, url, `type`, 
                category_name, media, keywords, style, channel_id, channel_name, audiourl, videourl, 
                image, start_time, content)
                value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE title = title"""

            cursor.execute(sql, (
                article['pid'], article['title'], card['id'], card['title'], card['url'],
                card['type'], article['categoryName'], card['media'],
                json.dumps(card['keywords']),
                card['style'], card['channelId'], card['channelName'], card['audiourl'],
                card['videourl'], json.dumps(card['image']), card['startTime'], article['content']))
            if article['related'] is not None:
                for line in article['related']:
                    articles.append(line['url'])
            print(len(articles))
            connection.commit()
        except Exception as e:
            print(e)
            print(card)
            print(article)

    articles = list(set(articles))
    while len(articles) > 0:
        articles.sort()
        article_url = articles.pop()
        article = get_article(article_url)
        try:
            sql = """insert into youdao_dict(pid, title, card_id, card_title, url, `type`, 
                category_name, media, style,  
                image, content)
                value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE title = title"""

            cursor.execute(sql, (
                article['pid'], article['title'], article['cardInfo']['id'],
                article['cardInfo']['title'], article['cardInfo']['url'],
                article['style']['type'], article['categoryName'], article['media'],
                article['style']['style'], article['cardInfo']['image'], article['content']))
            if article['related'] is not None:
                for line in article['related']:
                    if article_url > line['url'] and line['url'] not in articles:
                        articles.append(line['url'])
            connection.commit()
        except Exception as e:
            print(e)
            print(article)
    connection.close()


def crawler_by_link():
    global cards
    card_list, lastId = get_cards(None, '10')
    cards = cards + card_list
    # insert_into_mysql(cards)
    while len(card_list) > 0:
        card_list, lastId = get_cards(lastId, '10')
        cards = cards + card_list
    print('文章列表下载完成,共%d篇文章' % (len(cards)))
    insert_into_mysql()


def crawler_by_pid(pid):
    response = urllib.request.urlopen(articleUrl_prefix + str(pid) + articleUrl_suffix)
    result = response.read().decode('utf-8')
    # print(result.substring(120, 130))
    try:
        article = json.loads(result)
    except:
        print(article)
    return article


def insert_article(article):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root1234',
        db='dish',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = connection.cursor()
    try:
        sql = """insert into youdao_dict(pid, title, card_id, card_title, url, `type`, 
                category_name, media, style,  
                image, content)
                value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE title = title"""

        if 'id' in article['cardInfo'].keys():
            card_id = article['cardInfo']['id']
        else:
            card_id = 0
        if 'title' in article['cardInfo'].keys():
            card_title = article['cardInfo']['title']
        else:
            card_title = ''
        if 'url' in article['cardInfo'].keys():
            url = article['cardInfo']['url']
        else:
            url = articleUrl_prefix + str(article['pid'])
        if 'image' in article['cardInfo'].keys():
            image = article['cardInfo']['image']
        else:
            image = ''
        if 'style' in article.keys():
            type = article['style']['type']
            style = article['style']['style']
        else:
            type = ''
            style = ''

        cursor.execute(sql, (
            article['pid'], article['title'], card_id,
            card_title, url,
            type, article['categoryName'], article['media'],
            style, image, article['content']))
        connection.commit()
    except Exception as e:
        print(e)
        print(article)
    finally:
        connection.close()


if __name__ == '__main__':
    pid = 1666387
    while pid > 0:
        print(pid)
        article = crawler_by_pid(pid)
        if 'title' in article.keys():
            print(article['title'])
            insert_article(article)
        pid = pid - 1
