# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3,os,re   
from datetime import date, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "project.db")

class GittrendingScrapyPipeline:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS git_trending(
            repo_name VARCHAR(50),
            repo_language VARCHAR(50),
            repo_star_total INTEGER,
            repo_star_today_increase INTEGER,
            repo_spider_date DATE,
            repo_score INTEGER DEFAULT 0,
            PRIMARY KEY(repo_name,repo_spider_date)
        )''')
            
        self.conn.commit()
        print("数据库初始化完成")


    def process_item(self, item, spider):

        # 清洗一下数据
        raw_star_total = item.get('repo_star_total','0')
        item['repo_star_total'] = int(str(raw_star_total).replace(',','')) if raw_star_total else 0

        raw_star_today_increase = item.get('repo_star_today_increase','0')
        match = re.search(r'\d+',str(raw_star_today_increase))
        item['repo_star_today_increase'] = int(match.group()) if match else 0

        try:

            sql = '''
        INSERT OR REPLACE INTO git_trending (repo_name,repo_language,repo_star_total,repo_star_today_increase,repo_spider_date)
        VALUES (?,?,?,?,?)
        '''
            self.cursor.execute(sql,(
                item['repo_name'],
                item['repo_language'],
                item['repo_star_total'],
                item['repo_star_today_increase'],
                item['repo_spider_date']
            ))

            self.conn.commit()

            # 存完之后立刻评分
            score = self.calculate_score(item)
            self.cursor.execute(
                'UPDATE git_trending SET repo_score=? WHERE repo_name=? AND repo_spider_date=?',
                (score,item['repo_name'],item['repo_spider_date'])
            )
            self.conn.commit()

        except Exception as e:
            print(e)

        return item
    
    def calculate_score(self,item):

        score = 0
        
        # 今日增长量
        if item['repo_star_today_increase'] < 100:
            score += 20
        elif 100 < item['repo_star_today_increase'] < 1000:
            score += 30
        elif 1000 < item['repo_star_today_increase'] < 10000:
            score += 40     
        elif item['repo_star_today_increase'] > 10000:
            score += 45     

        # 项目基数小但增长快 = 潜力股
        if item['repo_star_total'] < 1000:
            score += 50
        elif 1000 < item['repo_star_total'] < 10000:
            score += 35
        elif 1000 < item['repo_star_total'] < 100000:
            score -= 10
        elif item['repo_star_total'] > 100000:
            score -= 20

        # 连续上榜天数-这里查历史
        consecutive = self.get_consecutive_days(item['repo_name'])
        score += (consecutive-1) * 30

        score = min(score,100)

        return score

    def get_consecutive_days(self,repo_name):
        today = date.today()
        count = 0
            
        # 从今天往前推，最多查30天
        for i in range(30):
            date_01 = (today - timedelta(days=i))
            self.cursor.execute(
                'SELECT 1 FROM git_trending WHERE repo_name=? AND repo_spider_date=?',
                (repo_name, date_01)
            )
            if self.cursor.fetchone():
                count += 1
            else:
                break  # 遇到断档就停，不连续了
            
        return count


    def close_spider(self,spider):
        # 采集结束，打印当日报告
        today = date.today()

        try:
            self.cursor.execute(
            'SELECT repo_name,repo_language,repo_star_today_increase,repo_score FROM git_trending WHERE repo_spider_date=? ORDER BY repo_score DESC LIMIT 10',(today,)
            )
            print(f"\n今日 top10热门项目({today})")
        except Exception as e:
            print(e)
            pass

        for row in self.cursor.fetchall():
            print(f"{row[0]} | {row[1]} | +{row[2]}stars | score:{row[3]}")

        self.cursor.close()
        self.conn.close()