from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from lyspider import settings

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(URL(**settings.DATABASE))


def create_table(engine):
    """
    创建表
    """
    DeclarativeBase.metadata.create_all(engine)


class GNY(DeclarativeBase):
    __tablename__ = 'rival_sales'
    id = Column(Integer, primary_key=True)
    wrapper_name = Column('wrapper_name')  # 爬虫名
    crawl_date = Column('craw_date', Date)  # 抓取日期
    type = Column('type', String)  # 类型 国内游还是境外游
    function = Column('function', String)  # 跟团游 自由行 目的地参团
    departure = Column('departure', String)  # 出发地
    arrive = Column('arrive', String)  # 目的地
    title = Column('title', Text)  # 产品标题
    url = Column('url', Text)  # 产品url
    price = Column('price', Numeric)  # 价格
    insert_time = Column('insert_time', DateTime)  # 插入时间
    sales = Column('dim1', Text)  # 销量
    satisfaction = Column('dim2', Text)  # 满意度
    evaluation = Column('dim3', Text)  # 评价
