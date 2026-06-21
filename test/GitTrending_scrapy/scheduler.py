import os,sys
from datetime import datetime 

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

# Scrapy 核心模块
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# 定时调度模块
from apscheduler.schedulers.blocking import BlockingScheduler
# 导入spider
from GitTrending_scrapy.spiders.GITthrending_spider import GitthrendingSpiderSpider


# 封装spider为函数
def run_gittrending_spider():
    # 加载Scrapy项目的配置(自动读取settings.py配置)
    process = CrawlerProcess(get_project_settings())

    # 启动爬虫
    process.crawl(GitthrendingSpiderSpider)

    # 启动爬虫(会阻塞当前线程,直至爬虫采集完成)
    print(f"[{datetime.now()}] GitHub Trending 采集程序开始启动......")
    process.start()
    print(f"[{datetime.now()}] GitHub Trending 采集程序完成......")


# 将爬虫函数加入调度器
if __name__ == "__main__":
    # 创建调度器
    scheduler = BlockingScheduler()

    # 每天早上8点整执行
    scheduler.add_job(
        run_gittrending_spider,
        'cron',
        hour = 10,
        minute = 0,
        id='GitTrending_crawler'
    )

    print("调度器已启动，爬虫将每天10点整自动运行一次...")
    try:
        scheduler.start()
    except Exception as e:
        print(e)