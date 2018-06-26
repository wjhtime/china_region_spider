import requests
from lxml import etree
import os
import time
import local_mysql
from requests.adapters import HTTPAdapter
import header

# 打印当前时间
def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 省
provinces = []

base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'

requests = requests.session()
requests.headers = header.header
# 重试5次
requests.mount('http://', HTTPAdapter(max_retries=5))
response = requests.get(base_url)
response.encoding = 'gb2312'

urls = etree.HTML(response.text).xpath("//tr[@class='provincetr']/td/a/@href")
names = etree.HTML(response.text).xpath("//tr[@class='provincetr']/td/a/text()")

for i in range(len(urls)):
    p_code = 0
    name = names[i]
    code = os.path.splitext(urls[i])[0]
    url = base_url + urls[i]
    item = {'p_code': 0, 'url': url, 'code': code, 'name': name, 'level': 1}
    provinces.append(item)
    print(name, code, url, 1, now())

local_mysql.save(provinces)

print('province over ============================')




provinces = local_mysql.select(1)

for province in provinces:
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

print('city over ============================')




cities = local_mysql.select(2)

for city in cities:
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

print('county over ============================')




counties = local_mysql.select(3)

for county in counties:
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

print('town over ============================')




towns = local_mysql.select(4)

for town in towns:
    villages = []
    village_res = requests.get(town[4])
    village_res.encoding = 'gb2312'
    base_url = os.path.dirname(town[4]) + '/'

    codes = etree.HTML(village_res.text).xpath("//tr[@class='villagetr']/td[1]/text()")
    names = etree.HTML(village_res.text).xpath("//tr[@class='villagetr']/td[3]/text()")

    for i in range(len(codes)):
        p_code = town[2]
        code = codes[i]
        name = names[i]
        item = {'p_code': p_code, 'code': code, 'name': name, 'level': 5, 'url':''}
        villages.append(item)
        print(name, code, 5, now())
    local_mysql.save(villages)

print('village over ============================')