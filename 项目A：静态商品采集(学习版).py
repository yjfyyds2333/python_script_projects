# ===============项目A:模拟跨境电商独立站静态商品采集（学习版）===============
import requests
from lxml import etree 
import os 
import time,random
import pandas as pd
from datetime import datetime
import logging


# 切换文件目录
dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

# 配置日志
filename = f"项目A_抓取日志_{datetime.now().strftime("%Y%m%d")}.log"
logging.basicConfig(
    level=logging.INFO,
    encoding='utf-8',
    handlers=[
        logging.FileHandler(filename),
        logging.StreamHandler()
    ],
    format="%(asctime)s - %(levelname)s - %(message)s"
)

base_url = "http://books.toscrape.com/catalogue/"
current_page_url = "http://books.toscrape.com/catalogue/page-1.html"

# 伪装请求头
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}

results = []
page_script = 0

while True:
    logging.info(f"正在抓取：{current_page_url}")
    time.sleep(random.uniform(1.5,2.5))

    # 1. 请求 current_page_url,拿到源码,转为tree
    # 1. 请求 current_page_url,拿到源码,转为tree
    try:
        response = requests.get(current_page_url,headers=headers)
    except TimeoutError:
        logging.error('获取网页超时')

    html_text = response.text
    html_tree = etree.HTML(html_text)

    # 1.先定位所有商品卡片的"容器"(大区快)
    # 用//定位全局，@class 精准匹配
    articles = html_tree.xpath('//article[@class="product_pod"]')

    # 2.提取数据
    for i,article in enumerate(articles):
        try:
            # 在当前大区块下(注意用.//开头),继续提取书名和价格
            # 提取 a 标签的 title 属性
            title = article.xpath('.//h3/a/@title')[0]
            # 提取 p 标签里的文本内容
            price = article.xpath('.//p[@class="price_color"]/text()')[0]
            # 是否有货
            is_instock = article.xpath('.//p[@class="instock availability"]/text()')[1].strip()

            results.append({
                '书名': title,
                '价格': price,
                '库存状态': is_instock
            })
        except Exception as e:
            logging.warning(e)
            pass

    # 抓取三页
    page_script += 1 
    logging.info(f'第{page_script}页抓取完成!')
    if page_script >= 3:
        break

    # 3.寻找下一页按钮的 href
    next_btn = html_tree.xpath('//li[@class="next"]/a/@href')

    # 4.判断是否还有下一页
    if next_btn:
        next_url = next_btn[0]
        current_page_url = base_url + next_url
    else:
        # 没有 next 按钮,说明到底了,退出循环
        logging.info("抓取完毕!")
        break

try:
    # 循环结束，一键导出
    filename = f'项目A_前3页的书本数据_{datetime.now().strftime("%Y%m%d")}.csv'
    df = pd.DataFrame(results)
    df.to_csv(filename,index=False)
    logging.info(f'程序结束,成功导出数据到{filename}')
except Exception as e:
    logging.error(f'出错了,问题是:{e}')



