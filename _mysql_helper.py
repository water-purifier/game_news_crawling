import pymysql.cursors, os
from dotenv import load_dotenv


class MysqlDB:
    def __init__(self):
        load_dotenv()

        _host = os.getenv('DB_HOST')
        _port = int(os.getenv('DB_PORT'))
        _user = os.getenv('DB_USER')
        _password = os.getenv('DB_PASS')
        _database = os.getenv('DB_NAME')
        self.conn = pymysql.connect(
            host=_host,
            port=_port,
            user=_user,
            password=_password,
            database=_database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def select(self, query):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def selectOne(self, query, tup):
        with self.conn.cursor() as cursor:
            cursor.execute(query, tup)
            result = cursor.fetchone()
            return result

    def select_by(self, query, tup):
        with self.conn.cursor() as cursor:
            cursor.execute(query, tup)
            return cursor.fetchall()

    def exec(self, query, tup):
        with self.conn.cursor() as cursor:
            cursor.execute(query, tup)
            self.conn.commit()
            return cursor.lastrowid

    def insertR(self, query, tup):
        with self.conn.cursor() as cursor:
            cursor.execute(query, tup)
            self.conn.commit()
            return cursor.lastrowid

    def updateR(self, query, tup):
        with self.conn.cursor() as cursor:
            cursor.execute(query, tup)
            self.conn.commit()
            return cursor.lastrowid

    def selectCount(self, _table, _field, _value):
        with self.conn.cursor() as cursor:
            query = "select count(*) as cnt from " + _table + " where " + _field + "=%s"
            cursor.execute(query, (_value))
            result = cursor.fetchone()
            return result['cnt']

    def checkInsert(self, _table, _field, _value, _query, _tup):
        if (self.selectCount(_table, _field, _value)) == 0:
            lastid = self.insertR(_query, _tup)
            return lastid
        else:
            return self.selectOne("select id from " + _table + " where " + _field + "=%s", (_value))['id']
