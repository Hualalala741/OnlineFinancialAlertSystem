# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class XlnewsPipeline:
    def process_item(self, item, spider):
        print('打开数据库')
        item.save()
        print('关闭数据库')
        return item


