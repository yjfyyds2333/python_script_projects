# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from datetime import datetime

class FangtxScrapyPipeline:
    
    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017, maxPoolSize=5)
        self.db = self.client['fangtx']
        self.collection = self.db['fangtx']
        self.cache = []  # 缓存item
        self.batch_size = 20
        print('数据库初始化完成')

    def process_item(self, item, spider):
        # data = {
        #     'house_id':item['house_id'],
        #     'house_title': item['house_title'],
        #     'house_total_price': item['house_total_price'],
        #     'house_unix_price': item['house_unix_price'],
        #     'house_type': item['house_type'],
        #     'house_square': item['house_square'],
        #     'house_towards': item['house_towards'],
        #     'house_floors': item['house_floors'],
        #     'house_community': item['house_community'],
        #     'house_area': item['house_area'],
        # }

        # self.cache.append(data)
        # # 缓存满批量插入
        # if len(self.cache) >= self.batch_size:
        #     self.collection.insert_many(self.cache)
        #     self.cache.clear()

        # return item

        # 增量以及实时更新数据
        self.collection.update_one(
            {'house_id':item['house_id']},
                {
                '$set':{
                    'house_title':item.get('house_title'),
                    'house_unix_price':item.get('house_unix_price'),
                    'house_total_price':item.get('house_total_price'),
                    'last_update': datetime.now()
                    },
                '$push':{
                    'price_history':{
                        'house_total_price':item.get('house_total_price'),
                        'date': datetime.now()
                    } 
                }
            },
            upsert=True
        )
        return item 



    def close_spider(self, spider):
        # 爬虫结束，插入剩余缓存数据
        if self.cache:
            self.collection.insert_many(self.cache)
        # 关闭Mongo连接池，释放所有socket
        if self.client:
            self.client.close()