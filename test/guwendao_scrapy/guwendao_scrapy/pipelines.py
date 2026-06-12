# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class GuwendaoScrapyPipeline:
    # 初始化数据库
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Yjf15113137810',
            db='test'
        )

        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS poems (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255),
            author VARCHAR(20),
            age VARCHAR(20),
            content TEXT
        )        
        ''')
        self.conn.commit()
        print('数据库初始化完成')

    def process_item(self, item, spider):
        # # 过滤空数据（标题为空就不存）
        if not item['title']:
            return item
        if not item['author']:
            return item
        if not item['age']:
            return item
        if not item['content']:
            return item
            
        try:
            sql = '''INSERT INTO poems (title,author,age,content) 
            VALUES(%s,%s,%s,%s)
            '''
            # 现在三个参数都是 字符串，不是列表！
            self.cursor.execute(sql, (
                item['title'],
                item['author'],
                item['age'],
                item['content']
            ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"插入失败：{e}")
        return item

    # def __init__(self):
    #     self.conn = pymysql.connect(
    #         host='localhost',
    #         user='root',
    #         password='Yjf15113137810',
    #         db='test'
    #     )

    #     self.cursor = self.conn.cursor()
    #     self.cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS test3 (
    #         id INT PRIMARY KEY AUTO_INCREMENT,
    #         title VARCHAR(255),
    #         author VARCHAR(50),
    #         content VARCHAR(50)
    #     )        
    #     ''')
    #     self.conn.commit()
    #     print('数据库初始化完成')

    # def process_item(self, item, spider):
    #     # # 过滤空数据（标题为空就不存）
    #     if not item['title']:
    #         return item
    #     if not item['age']:
    #         return item
    #     if not item['category']:
    #         return item
            
    #     try:
    #         sql = '''INSERT INTO test3 (title,age,category) 
    #         VALUES(%s,%s,%s)
    #         ON DUPLICATE KEY UPDATE title=VALUES(title),age=VALUES(age),category=VALUES(category)
    #         '''
    #         # 现在三个参数都是 字符串，不是列表！
    #         self.cursor.execute(sql, (
    #             item['title'],
    #             item['age'],
    #             item['category']
    #         ))
    #         self.conn.commit()
    #     except Exception as e:
    #         self.conn.rollback()
    #         print(f"插入失败：{e}")
    #     return item

    # def close_spider(self,spider):
    #     self.cursor.close()
    #     self.conn.close()

        
