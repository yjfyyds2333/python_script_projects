from datetime import datetime   
from apscheduler.schedulers.blocking import BlockingScheduler

# 用 CrawlerProcess 在普通函数里启动Scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .fangtx_scrapy.spiders.fangtx_spider import FangtxSpiderSpider


# ----------------------
# 1. 封装链家爬虫为函数
# ----------------------
def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(FangtxSpiderSpider)

    # 启动爬虫（会阻塞当前线程，直到爬虫采集完成）
    print(f"[{datetime.now()}] 房天下爬虫开始启动...")
    process.start()
    print(f"[{datetime.now()}] 房天下爬虫采集完成！")

# ----------------------
# 2. 把爬虫函数加入调度器
# ----------------------
if __name__ == "__main__":
    # 创建调度器
    scheduler = BlockingScheduler()

    scheduler.add_job(
        run_spider,
        'cron',
        hour = 10,
        minutes=0,  # 测试用，改成1分钟
        id='fangtx_crawler'
    )

    # 启动调度器
    print("调度器已启动，爬虫将每天10点整自动运行一次...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("调度器已停止")