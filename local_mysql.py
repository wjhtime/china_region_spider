import pymysql
from database import db
import asyncio
import aiomysql

class local_mysql():

    def __init__(self):
        self.host = db['host']
        self.user = db['user']
        self.password = db['password']
        self.database = db['database']
        self.db = pymysql.connect(self.host, self.user, self.password, self.database)
        self.db.set_charset('utf8')

    # def save(self, rows):
    #     cursor = self.db.cursor()
    #     sql = "insert into china_regions(p_code, code, `name`, `url`, `level`) values('%s','%s','%s', '%s', '%s')"
    #     for row in rows:
    #         # 去重
    #         # if cursor.execute("select count(id) from china_regions where code=%s" % row['code']) == 0:
    #             cursor.execute(sql % (row['p_code'], row['code'], row['name'], row['url'], row['level']))
    #     self.db.commit()



    def select(self, level):
        cursor = self.db.cursor()
        sql = "select * from china_regions where level=%d" % level
        result = cursor.execute(sql)
        data = cursor.fetchmany(result)
        return data



    # aiomysql测试
    def save(self, rows):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.go(loop, rows))

    async def go(self, loop, rows):
        sql = "insert into china_regions(p_code, code, `name`, `url`, `level`) values('%s','%s','%s', '%s', '%s')"
        pool = await aiomysql.create_pool(host='localhost', port=3306,
                                          user='root', password='root',
                                          db='python', loop=loop, charset='utf8')
        for row in rows:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(sql % (row['p_code'], row['code'], row['name'], row['url'], row['level']))
                    await conn.commit()

        pool.close()
        await pool.wait_closed()
