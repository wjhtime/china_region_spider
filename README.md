# 中国省市地区爬虫


![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)
![npm](https://img.shields.io/npm/l/express.svg)



爬取中国城乡数据的爬虫，有请求重试机制，只要执行一行命令即可获取所有省市区，另有采集好的mysql版本数据 [传送门](https://github.com/wjhtime/china_regions)



## Requirements

- Python3
- Mysql
- requests
- lxml
- pymysql
- time
- os



## Quick Start

```python
python3 spider.py
```



## Feature

- 数据来源于国家统计局，网址：<http://www.stats.gov.cn/> ，总共846462条数据，记录了全中国的省、市、县、镇、村委会的所有地区数据。
- 网络请求异常重试，尝试5次，避免网络异常时爬取中断
- 反爬虫机制





## 表结构

| 字段     | 备注             |
| ------ | -------------- |
| id     | 主键             |
| p_code | 上一级编码          |
| code   | 编码             |
| name   | 名称             |
| url    | 当前的城市链接，供下一次采集 |
| level  | 级别             |



### 建表语句

```mysql
CREATE TABLE `china_regions` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `p_code` varchar(50) NOT NULL DEFAULT '' COMMENT '上一级编码',
  `code` varchar(50) NOT NULL DEFAULT '' COMMENT '编码',
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '名称',
  `url` varchar(200) NOT NULL DEFAULT '' COMMENT '链接',
  `level` tinyint(4) NOT NULL COMMENT '级别:1-省，2-市，3-县，4-镇，5-村委会',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```



## License

[MIT](https://github.com/wjhtime/china_region_spider/blob/master/LICENSE)