from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from lyspider.items import LyspiderItem
from datetime import *
from lyspider.resource import props
import json
from lyspider.resource import departure_cities as srcs
from lyspider.resource import destinations as dests
from lyspider.url_generator import URLGenerator
import time
import urllib.request
import logging
from scrapy.utils.log import configure_logging
from lyspider.tools import get_link_from_json

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='[%(asctime)s][%(process)d:%(thread)d][%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S %p',
    level=logging.WARNING
)

"""
1.抓取url: http://gny.ly.com/list?src=北京&dest=上海&prop=0
2.prop: 0代表全部 1代表跟团游 3代表自由行 5代表目的地参团
3.拿取所有的出发地城市列表和目的地城市列表
"""


class LySalesSpider(Spider):
    name = 'ly-gny-sales'
    allowed_domains = ['ly.com']

    url_generator = URLGenerator(srcs, dests)
    start_urls = url_generator.generate_urls()

    # start_urls = [
    #     "http://gny.ly.com/list?prop=0&src=%E5%8C%97%E4%BA%AC&dest=%E4%B8%8A%E6%B5%B7&label=buttom&action=list"
    # ]

    # 该方法主要是解析下一页的json数据
    def parse_next_page(self, response):
        json_response = json.loads(response.body_as_unicode())
        line_list = json_response['lineList']
        items = []
        for line in line_list:
            item = LyspiderItem()
            # 固定
            item['wrapper_name'] = 'ly-gny-spider'
            item['crawl_date'] = date.today()
            item['insert_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            item['type'] = '国内游'

            # 解析
            item['function'] = props[line['prop']]  # 1: 跟团游; 3: 自由行 5: 目的地参团
            item['departure'] = line['portCity']
            item['arrive'] = response.meta['dest']
            item['title'] = line['Title'] + "<" + line["subTitle"] + ">"
            item['url'] = "http://gny.ly.com" + get_link_from_json(line)
            item['price'] = float(line['tcPrice'])
            item['sales'] = line['trips']  # 整数
            item['evaluation'] = line['cmtCount']  # 字符串
            item['satisfaction'] = str(line['favRate']) + '%'  # 整数
            items.append(item)

        for item in items:
            yield item

    def parse(self, response):
        selector = Selector(response)
        recommends = selector.xpath("/html/body/div[@class='mainbody']/div[@class='container']" +
                                    "/div[@class='route-box']/div[@class='route-content recommend']" +
                                    "/div[@class='bd']/ul/li")
        normals = selector.xpath("/html/body/div[@class='mainbody']/div[@class='container']" +
                                 "/div[@class='route-box']/div[@class='route-content normal']" +
                                 "/div[@class='bd']/ul/li")
        # 总计多少条数据
        total_count = 0
        if not selector.xpath("/html/body/div[@class='mainbody']/div[@class='container']/div[@class='line-nav none']"):
            total_count = int(selector.xpath("/html/body/div[@class='mainbody']/div[@class='container']" +
                                             "/div[@class='line-nav ']/div[@class='hd']/a[1]/span/text()").extract()[0])

        # 出发城市, 目的地
        departure = urllib.request.unquote(
            selector.xpath("/html/head/link[1]/@href").re('^.*src=(.*)&dest=(.*?)&.*')[0])
        arrive = urllib.request.unquote(
            selector.xpath("/html/head/link[1]/@href").re('^.*src=(.*)&dest=(.*?)&.*')[1])

        total_page = 1
        # 总页数 = (total_count + 20 -1)/20
        if total_count <= 20:
            pass
        else:
            total_page = int((total_count + 19) / 20)

        urls = []
        if total_page != 1:
            for x in range(2, total_page + 1):
                url = "http://gny.ly.com/list/GetNextPageData?src={}&dest={}&prop=0&start={}".format(departure, arrive,
                                                                                                     x)
                urls.append(url)
        for url in urls:
            yield Request(url, callback=self.parse_next_page, meta={"dest": arrive})

        items = []
        if recommends:
            for recommend in recommends:
                item = LyspiderItem()
                # 固定
                item['wrapper_name'] = 'ly-gny-spider'
                item['crawl_date'] = date.today()
                item['insert_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                item['type'] = '国内游'
                # 解析
                item['function'] = recommend.xpath('a/div[1]/span[1]/text()').extract()[0]
                item['departure'] = departure
                item['arrive'] = arrive
                item['title'] = recommend.xpath('a/div[2]/h3/em/@title').extract()[0].strip()
                item['url'] = "http://gny.ly.com" + recommend.xpath('a/@href').extract()[0].strip()
                item['price'] = float(
                    recommend.xpath('a/div[2]/div[2]/div[@class="dr"]/p[1]/span/strong/text()').extract()[0].strip())
                # 销量
                regular_sales = recommend.xpath('a/div[2]/div[2]/div[2]/div[2]/p[1]/text()')
                irregular_sales = recommend.xpath('a/div[2]/div[2]/div[2]/div/p/text()')
                if regular_sales:
                    item['sales'] = int(regular_sales.re('^(\d+)人已购买')[0])
                    item['evaluation'] = recommend.xpath('a/div[2]/div[2]/div[2]/div[2]/p[2]/text()').re('^(\d+)')[0]
                    item['satisfaction'] = recommend.xpath('a/div[2]/div[2]/div[2]/div[1]/p[1]/text()').extract()[
                                               0] + "%"
                elif irregular_sales.re('^(\d+)人已购买'):
                    item['sales'] = irregular_sales.re('^(\d+)人已购买')[0]
                items.append(item)

        if normals:
            for normal in normals:
                item = LyspiderItem()
                item['wrapper_name'] = 'ly-gny-spider'
                item['crawl_date'] = date.today()
                item['insert_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                item['type'] = '国内游'
                # 解析
                item['function'] = normal.xpath('a/div[1]/span[1]/text()').extract()[0]
                item['departure'] = departure
                item['arrive'] = arrive
                item['title'] = normal.xpath('a/div[2]/h3/em/@title').extract()[0].strip()
                item['url'] = "http://gny.ly.com" + normal.xpath('a/@href').extract()[0].strip()
                item['price'] = float(
                    normal.xpath('a/div[2]/div[2]/div[@class="dr"]/p[1]/span/strong/text()').extract()[0].strip())
                # 销量
                regular_sales = normal.xpath('a/div[2]/div[2]/div[2]/div[2]/p[1]/text()')
                irregular_sales = normal.xpath('a/div[2]/div[2]/div[2]/div/p/text()')
                if regular_sales:
                    item['sales'] = int(regular_sales.re('^(\d+)人已购买')[0])
                    item['evaluation'] = normal.xpath('a/div[2]/div[2]/div[2]/div[2]/p[2]/text()').re('^(\d+)')[0]
                    item['satisfaction'] = normal.xpath('a/div[2]/div[2]/div[2]/div[1]/p[1]/text()').extract()[0] + "%"
                elif irregular_sales.re('^(\d+)人已购买'):
                    item['sales'] = irregular_sales.re('^(\d+)人已购买')[0]

                items.append(item)

        for item in items:
            yield item

