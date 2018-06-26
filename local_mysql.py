import pymysql

def save(rows):
    db = pymysql.connect('localhost', 'root', 'root', 'python')
    db.set_charset('utf8')
    cursor = db.cursor()
    sql = "insert into province_city2(p_code, code, `name`, `url`, `level`) values('%s','%s','%s', '%s', '%s')"
    for row in rows:
        # 去重
        # if cursor.execute("select count(id) from province_city where code=%s" % row['code']) == 0:
        cursor.execute(sql % (row['p_code'], row['code'], row['name'], row['url'], row['level']))
    db.commit()
    db.close()


def select(level):
    db = pymysql.connect('localhost', 'root', 'root', 'python')
    cursor = db.cursor()
    sql = "select * from province_city2 where level=%d" % level
    result = cursor.execute(sql)
    data = cursor.fetchmany(result)
    return data
