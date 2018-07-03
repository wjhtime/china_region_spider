import requests
from lxml import etree
import os
import time
from local_mysql import local_mysql
from requests.adapters import HTTPAdapter
import header
from multiprocessing import Process, cpu_count, Pool

# 打印当前时间
def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

local_mysql = local_mysql()

base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'

requests = requests.session()
requests.headers = header.header
# 重试5次
requests.mount('http://', HTTPAdapter(max_retries=5))


class province():

    def __init__(self):
        pass

    def crawler(self):
        # 省
        provinces = []
        response = requests.get(base_url)
        response.encoding = 'gb2312'

        urls = etree.HTML(response.text).xpath("//tr[@class='provincetr']/td/a/@href")
        names = etree.HTML(response.text).xpath("//tr[@class='provincetr']/td/a/text()")

        for i in range(len(urls)):
            p_code = 0
            name = names[i]
            code = os.path.splitext(urls[i])[0]
            url = base_url + urls[i]
            item = {'p_code': p_code, 'url': url, 'code': code, 'name': name, 'level': 1}
            provinces.append(item)
            print(name, code, url, 1, now())

        local_mysql.save(provinces)
        del provinces
        print('province over ============================')



class city():

    def crawler(self):
        provinces = local_mysql.select(1)
        p = Pool(processes=cpu_count())
        for province in provinces:
            p.apply_async(self.process, args=(province,))
        p.close()
        p.join()
        print('city over ============================')

    def process(self, province):
        cities = []
        response = requests.get(province[4])
        response.encoding = 'gb2312'

        base_url = os.path.dirname(province[4]) + '/'
        codes = etree.HTML(response.text).xpath("//tr[@class='citytr']/td[1]/a/text()")
        names = etree.HTML(response.text).xpath("//tr[@class='citytr']/td[2]/a/text()")
        urls = etree.HTML(response.text).xpath("//tr[@class='citytr']/td[1]/a/@href")

        for i in range(len(codes)):
            p_code = province[2]
            url = base_url + urls[i]
            code = codes[i]
            name = names[i]
            item = {'p_code': p_code, 'url': url, 'code': code, 'name': name, 'level': 2}
            cities.append(item)
            print(name, code, url, 2, now())
        local_mysql.save(cities)
        del cities


class county():

    def process(self, city):
        counties = []
        counties_res = requests.get(city[4])
        counties_res.encoding = 'gb2312'
        base_url = os.path.dirname(city[4]) + '/'

        codes = etree.HTML(counties_res.text).xpath("//tr[@class='countytr']/td[1]/a/text()")
        names = etree.HTML(counties_res.text).xpath("//tr[@class='countytr']/td[2]/a/text()")
        urls = etree.HTML(counties_res.text).xpath("//tr[@class='countytr']/td[1]/a/@href")

        for i in range(len(codes)):
            p_code = city[2]
            url = base_url + urls[i]
            code = codes[i]
            name = names[i]
            item = {'p_code': p_code, 'url': url, 'code': code, 'name': name, 'level': 3}
            counties.append(item)
            print(name, code, url, 3, now())
        local_mysql.save(counties)
        del counties

    def crawler(self):
        cities = local_mysql.select(2)
        p = Pool(processes=cpu_count())
        for city in cities:
            p.apply_async(self.process, args=(city,))
        p.close()
        p.join()

        print('county over ============================')


class town():
    def process(self, county):
        towns = []
        town_res = requests.get(county[4])
        town_res.encoding = 'gb2312'
        base_url = os.path.dirname(county[4]) + '/'

        codes = etree.HTML(town_res.text).xpath("//tr[@class='towntr']/td[1]/a/text()")
        names = etree.HTML(town_res.text).xpath("//tr[@class='towntr']/td[2]/a/text()")
        urls = etree.HTML(town_res.text).xpath("//tr[@class='towntr']/td[1]/a/@href")

        for i in range(len(codes)):
            p_code = county[2]
            url = base_url + urls[i]
            code = codes[i]
            name = names[i]
            item = {'p_code': p_code, 'url': url, 'code': code, 'name': name, 'level': 4}
            towns.append(item)
            print(name, code, url, 4, now())
        local_mysql.save(towns)
        del towns


    def crawler(self):
        counties = local_mysql.select(3)
        p = Pool(cpu_count())
        for county in counties:
            p.apply_async(self.process, args=(county, ))
        p.close()
        p.join()

        print('town over ============================')



class village():
    def process(self, town):
        villages = []
        village_res = requests.get(town[4])
        village_res.encoding = 'gb2312'

        codes = etree.HTML(village_res.text).xpath("//tr[@class='villagetr']/td[1]/text()")
        names = etree.HTML(village_res.text).xpath("//tr[@class='villagetr']/td[3]/text()")

        for i in range(len(codes)):
            p_code = town[2]
            code = codes[i]
            name = names[i]
            item = {'p_code': p_code, 'code': code, 'name': name, 'level': 5, 'url': ''}
            villages.append(item)
            print(name, code, 5, now())
        local_mysql.save(villages)
        del villages

    def crawler(self):
        towns = local_mysql.select(4)
        p = Pool(cpu_count())
        for town in towns:
            p.apply_async(self.process, args=(town, ))
        p.close()
        p.join()

        print('village over ============================')


def main():
    start = time.time()
    province().crawler()
    city().crawler()
    county().crawler()
    town().crawler()
    village().crawler()
    print("共耗时{0}s". format(time.time() - start))

if __name__ == '__main__':
    main()
