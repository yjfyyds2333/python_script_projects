import scrapy
import os
import re
dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

import sys,json
from pathlib import Path
# 拿到项目根目录 fangtx_scrapy
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

# 绝对导入，不用点点点
from items import FangtxScrapyItem

with open('citys_url.json','r') as f:
    urls = json.load(f)

class FangtxSpiderSpider(scrapy.Spider):
    name = "fangtx_spider"
    allowed_domains = ["fang.com"]

    start_urls = [url for url in urls]

    def parse(self, response):
        '''主页，找出各个城市的网址'''
        cards = response.xpath('//dl[@class="clearfix "]')
        if not cards:
            print("当前页面无房源卡片，URL：", response.url)
            return

        for card in cards:
            item = FangtxScrapyItem()
            # 拼接详情完整url
            href = card.xpath('.//h4[@class="clearfix"]/a/@href').get()

            match = re.search(r'(\d+).htm',href)
            if match:
                house_id = match.group(1)
            else:
                house_id = ''

            if not house_id:
                continue

            if not href:
                print(f"详细页获取失败:{href}")
                continue

            # 清洗数据
            raw_unix_price = card.xpath('.//dd[@class="price_right"]/*[2]/text()').get('')
            if not raw_unix_price:
                print("未获取到单价数据")
                continue

            match = re.search(r'(\d+)',raw_unix_price)
            if not match:
                print("未找到数字")
                continue
            
            clean_unix_price = match.group().strip()

            raw_list = card.xpath('.//p[@class="tel_shop"]/text() | .//p[@class="tel_shop"]/a/text()').getall()
            # 去除空格、过滤分隔符|
            clean_data = [s.strip() for s in raw_list if s.strip() != "|"]
            # clean_data = ['3室2厅', '169.36㎡', '中层', '（共24层）', '东南向']

            house_type = clean_data[0]    # 3室2厅

            raw_house_square =  clean_data[1]  #169.36㎡
            clean_house_square = re.sub(r'[^\d.]','',raw_house_square) 
    
            raw_house_floors =  clean_data[3]  # （共24层）
            match = re.search(r'(\d+)',raw_house_floors)
            clean_house_floors = match.group(1)

            house_towards = clean_data[4] # 东南向

            item['house_id'] = house_id
            item['house_title'] = card.xpath('.//span[@class="tit_shop"]/text()').get('').strip()
            item['house_total_price'] = card.xpath('.//span[@class="red"]/b/text()').get('').strip()
            item['house_unix_price'] = clean_unix_price
            item['house_type'] = house_type
            item['house_square'] = clean_house_square
            item['house_floors'] = clean_house_floors
            item['house_towards'] = house_towards
            item['house_community'] = card.xpath('.//p[@class="add_shop"]/a/@title').get('')
            item['house_area'] = card.xpath('.//p[@class="add_shop"]/*[2]/text()').get('')

            if not item['house_area']:
                self.logger.warning("当前房源缺少地区字段，跳过本条")
                continue

            yield item

            # 翻页逻辑修复：urljoin拼接完整地址
            next_href = response.xpath('//p[@class="last"]/*[1]/a/@href').get()
            if next_href:
                next_full_url = response.urljoin(next_href)
                yield scrapy.Request(url=next_full_url, callback=self.parse)

        pass

    