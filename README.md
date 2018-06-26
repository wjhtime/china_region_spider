# china_region_spider
爬取中国城乡数据的爬虫



python3 spider.py



## 特点

- 请求失败时会自动重试，默认5次
- 使用requests包







## 表结构



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



