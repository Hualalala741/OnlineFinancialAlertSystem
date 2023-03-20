# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

from twisted.enterprise import adbapi


# 异步更新操作
class Scrapy1Pipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )
        dbpool = adbapi.ConnectionPool('pymysql',**adbparams)
        #返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常

    def do_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        insert_sql ="insert into news(link,title,date,source,article) VALUES (%s,%s,%s,%s,%s)"

        cursor.execute(insert_sql, (item['link'], item['title'],item['date'],item['source'],item['article']))

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print(failure)



# class Scrapy1Pipeline:
#     def process_item(self, item, spider):
#         try:
#             res = dict(item)
#             line = res['title']
#             self.file.write(line+'\n')
#         except:
#             pass
#         # print(item)
#         # return item
#
#     def open_spider(self,spider):
#         self.file = open('items.txt','w', encoding='utf-8')
#
#     def close_spider(self,spider):
#         self.file.colse()



