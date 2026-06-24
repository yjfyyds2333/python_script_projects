# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import openpyxl,os

os.makedirs("output",exist_ok=True)


class GushiwenScrapyPipeline:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client["Poems"]
        self.collection = self.db["poems"]
        print("数据库初始化完成!")

        pass

    def process_item(self, item, spider):
        
        self.collection.update_one(
            {'poem_id':item["poem_id"]},{
                '$set':{
                    'title':item['title'],
                    'dynasty':item['dynasty'],
                    'author':item['author'],
                    'text':item['text'],
                    'translation':item['translation'],
                    'comment':item['comment'],
                }
            },
            upsert=True
        )

        return item
    
    def close_spider(self, spider):
        self.client.close()
        
class ExcelPipeline:
    def open_spider(self,spider):
        """爬虫启动时:创建工作簿和表头"""
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.append(['title','author','dynasty','text','translation'])

    def process_item(self, item, spider):
        """每条数据：写一行"""
        self.ws.append([
            item.get('title', ''),
            item.get('author', ''),
            item.get('dynasty', ''),
            item.get('text', ''),
            item.get('translation', ''),
        ])
        return item  # 别忘了return，否则后续Pipeline拿不到

    def close_spider(self, spider):
        """爬虫结束时：保存文件"""
        self.wb.save('./output/gushiwen.xlsx')