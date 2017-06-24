# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LyspiderItem(scrapy.Item):
    wrapper_name = scrapy.Field()  # 爬虫名
    crawl_date = scrapy.Field()  # 抓取日期
    type = scrapy.Field()  # 类型 国内游还是境外游
    function = scrapy.Field()  # 跟团游 自由行 目的地参团
    departure = scrapy.Field()  # 出发地
    arrive = scrapy.Field()  # 目的地
    title = scrapy.Field()  # 产品标题
    url = scrapy.Field()  # 产品url
    price = scrapy.Field()  # 价格
    insert_time = scrapy.Field()  # 插入时间
    sales = scrapy.Field()  # 销量
    satisfaction = scrapy.Field()  # 满意度
    evaluation = scrapy.Field()  # 评价