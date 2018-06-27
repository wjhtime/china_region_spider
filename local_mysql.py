import pymysql
from database import db

class local_mysql():

    def __init__(self):
        self.host = db['host']
        self.user = db['user']
        self.password = db['password']
        self.database = db['database']
        self.db = pymysql.connect(self.host, self.user, self.password, self.database)
        self.db.set_charset('utf8')

    def save(self, rows):
        cursor = self.db.cursor()
        sql = "insert into china_regions(p_code, code, `name`, `url`, `level`) values('%s','%s','%s', '%s', '%s')"
        for row in rows:
            # 去重
            # if cursor.execute("select count(id) from province_city where code=%s" % row['code']) == 0:
            cursor.execute(sql % (row['p_code'], row['code'], row['name'], row['url'], row['level']))
        self.db.commit()



    def select(self, level):
        cursor = self.db.cursor()
        sql = "select * from china_regions where level=%d" % level
        result = cursor.execute(sql)
        data = cursor.fetchmany(result)
        return data
