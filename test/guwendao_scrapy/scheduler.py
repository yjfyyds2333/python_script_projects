# 切换到当前目录
import os 
dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

# 导入Scrapy相关模块，解决事件循环冲突
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime
from guwendao_scrapy.spiders.gushidao_spider import GushidaoSpiderSpider
import threading

# 导入APScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

# ----------------------
# 1. 封装链家爬虫为函数
# ----------------------
def run_gushiwen_spider():
    """在普通函数里安全启动Scrapy爬虫，避免和APScheduler冲突"""
    # 加载Scrapy项目的配置（自动读取settings.py里的配置）
    process = CrawlerProcess(get_project_settings())
    
    # 启动你的古诗文爬虫，这里的'gushiwen'要和你爬虫文件里的name一致
    process.crawl(GushidaoSpiderSpider)
    
    # 启动爬虫（会阻塞当前线程，直到爬虫采集完成）
    print(f"[{datetime.now()}] 古诗文爬虫开始启动...")
    process.start()
    print(f"[{datetime.now()}] 古诗文爬虫采集完成！")

def stop_scheduler(scheduler):
    scheduler.shutdown(wait=False)
    print(f'[{datetime.now()}]1分钟倒计时结束,自动停止程序')

# ----------------------
# 2. 把爬虫函数加入调度器
# ----------------------
if __name__ == "__main__":
    # 创建调度器
    scheduler = BlockingScheduler()

    # 测试用：每1分钟触发一次爬虫（方便你验证是否自动启动）
    scheduler.add_job(
        run_gushiwen_spider,
        'interval',
        minutes=2,  # 测试用，改成1分钟
        id='gushiwen_crawler'
    )

    # threading.Timer(60,stop_scheduler,args=(scheduler,)).start()

    # 正式用：每天早上8点触发一次爬虫（后面可以替换这个）
    # scheduler.add_job(
    #     run_lianjia_spider,
    #     'cron',
    #     hour=8,
    #     minute=0,
    #     id='lianjia_crawler'
    # )

    # 启动调度器
    print("调度器已启动，古诗文爬虫将每1分钟自动运行一次...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("调度器已停止")