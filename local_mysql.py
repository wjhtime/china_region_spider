import pymysql

class local_mysql():

    host = "localhost"
    user = "root"
    password = "root"
    database = "python"

    def __init__(self):
        pass

    def save(self, rows):
        db = pymysql.connect(self.host, self.user, self.password, self.database)
        db.set_charset('utf8')
        cursor = db.cursor()
        sql = "insert into china_regions(p_code, code, `name`, `url`, `level`) values('%s','%s','%s', '%s', '%s')"
        for row in rows:
            # 去重
            # if cursor.execute("select count(id) from province_city where code=%s" % row['code']) == 0:
            cursor.execute(sql % (row['p_code'], row['code'], row['name'], row['url'], row['level']))
        db.commit()
        db.close()


    def select(self, level):
        db = pymysql.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "select * from china_regions where level=%d" % level
        result = cursor.execute(sql)
        data = cursor.fetchmany(result)
        return data
