# -*- coding: UTF-8 -*-   #声明文件编码为utf-8

from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
import codecs


class CitySpider(Spider):
    name = 'city'
    allowed_domains = ['ly.com']
    start_urls = ['http://gny.ly.com/list?prop=0&dest=%E4%B8%8A%E6%B5%B7&src=%E9%84%82%E5%B0%94%E5%A4%9A%E6%96%AF']

    def parse(self, response):
        selector = HtmlXPathSelector(response)
        # 出发地字母分类
        class4 = selector.xpath('//*[@id="gnyallist-al"]/div/div[2]/div[1]/following-sibling::div')
        # 目的地省份
        provinces = selector.xpath('/html/body/div[2]/div[1]/div/div[2]/div[4]/div[2]/dl')

        # departure_cities = []
        # for one in class4:
        #     in_class = one.xpath("dl")
        #     for element in in_class:
        #         info = element.xpath("dd/a/text()").extract()
        #         departure_cities += info
        #
        # with codecs.open("tmp.txt", 'w', encoding='utf-8') as f:
        #     f.write(str(departure_cities))
        #     f.close()

        arrive_cities = []
        for province in provinces:
            info = province.xpath('dd/a/text()').extract()
            arrive_cities += info

        with codecs.open("tmp.txt", 'w+', encoding='utf-8') as f:
            f.write(str(arrive_cities))
            f.close()
