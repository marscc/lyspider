# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from lyspider.models import GNY, db_connect, create_table
from scrapy.exceptions import DropItem
import redis


# 去重pipeline
class DuplicatePipeline(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def process_item(self, item, spider):
        if self.r.sismember('urls', item['url']):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.r.sadd('urls', item['url'])
            return item


# 数据库操作pipeline
class DataBasePipeline(object):
    def __init__(self):
        """
        初始化数据库连接和sessionmaker
        """
        engine = db_connect()
        # create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        item入库
        :param item:
        :param spider:
        :return:
        """
        session = self.Session()
        gny = GNY(**item)

        try:
            session.add(gny)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

        return item
