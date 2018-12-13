import pymysql


def connect():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root1234',
        db='dish',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
