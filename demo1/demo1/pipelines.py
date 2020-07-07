# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from . import mysql_utils

localhost = "localhost"
port = 3306
user = "root"
password = "123456"
db = "a91"
charset = "utf8"


class Demo1Pipeline:
    exchange_rate = 8.5309

    def process_item(self, item, spider):
        if spider.name == "books":
            price = float(item['price'][1:]) * self.exchange_rate
            item['price'] = '￥%.2f' % price
            return item
        elif spider.name == "91":
            pass


class MysqlPipeline(object):
    # 定义构造器，初始化要写入的文件
    def __init__(self):
        mysql_utils.init_db()

    # 重写close_spider回调方法，用于关闭数据库资源
    def close_spider(self, spider):
        print('----------关闭数据库资源-----------')
        mysql_utils.close_db()

    def process_item(self, item, spider):
        if spider.name == '91' and item is not None:
            print(item)
            l = []
            v = []
            keys = item.keys()
            for k in keys:
                v.append(item.get(k))
            l.append(v)
            mysql_utils.insert_list(keys, "91", l)
        # mysql_utils.insert_item()
