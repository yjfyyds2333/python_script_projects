import scrapy
import re
from gushiwen_scrapy.items import GushiwenScrapyItem
import os 
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

from dotenv import load_dotenv
load_dotenv()

cookies = os.getenv("COOKIE")

class GushiwenSpiderSpider(CrawlSpider):
    name = "gushiwen_spider"
    allowed_domains = ["guwendao.net"]
    start_urls = ["https://www.guwendao.net/default_1.aspx"]

    # Rule = 告诉Scrapy"从这个页面里提取哪些链接，交给哪个callback处理"
    rules = (
        # 提取下一页链接-->继续跟踪
        Rule(LinkExtractor(allow=r'/default_\d+\.aspx'),follow=True),
        # 详细页链接-交给pare_detail处理
        Rule(LinkExtractor(allow=r'/shiwenv_\w+\.aspx'),callback="parse_detail"),
    )

    def parse_detail(self,response):
        "详细页采集"
        item = GushiwenScrapyItem()

        part_detail_url = response.url
        match = re.search(r'_(.*?)\.aspx',part_detail_url)

        if match:
            poem_id = match.group(1)
        else:
            print('未获取到poem_id')
            return

        title = response.xpath('//div[@class="left"]/*[2]/*[1]/*[2]/*[1]/text()').get('').strip()

        raw_dynasty = response.xpath('//div[@class="left"]/*[2]/*[1]/*[2]/*[2]/*[2]/text()').get('').strip()
        clean_dynasty = re.sub(r'[()〔〕]','',raw_dynasty)

        author = response.xpath('//div[@class="left"]/*[2]/*[1]/*[2]/*[2]/*[1]/img/@alt').get('').strip()
        raw_text_1 = response.xpath('//div[@class="contson"]/p/text()').getall()
        raw_text_2 = response.xpath('//div[@class="contson"]/text()').getall()

        if raw_text_1:
            raw_text = raw_text_1
        elif raw_text_2:
            raw_text = raw_text_2
        else:
            print("未找到译文")
            return          
        
        if raw_text:
            clean_text = '\n'.join(s.strip() for s in raw_text if s.strip())
        else:
            print("未找到译文")
            return

        raw_translation_1 = response.xpath('//div[@class="left"]/*[3]/*[1]/*[2]/text()').getall()
        raw_translation_2 = response.xpath('//div[@class="left"]/*[3]/*[1]/*[3]/text()').getall()

        if raw_translation_1:
            raw_translation = raw_translation_1
        elif raw_translation_2:
            raw_translation = raw_translation_2
        else:
            print('未找到译文')
            return

        if raw_translation:
            clean_translation = '\n'.join(s.replace('\n','').strip() for s in raw_translation if s.replace('\n','').strip())
        else:
            print("未找到译文")
            return
        
        raw_comment = response.xpath('//div[@class="left"]/*[3]/*[1]/*[3]/text()').getall()
        if raw_comment:
            clean_comment = '\n'.join(s.replace('\n','').strip() for s in raw_comment if s.replace('\n','').strip())
        else:
            print("未找到注释")
            return

        img_url = response.xpath('//div[@class="left"]/*[2]/*[1]/*[2]/*[2]/*[1]/img/@src').get('')

        if img_url:
            item['file_urls'] = [img_url]
        else:
            item['file_urls'] = []

        item['poem_id'] = poem_id
        item['title'] = title
        item['dynasty'] = clean_dynasty
        item['author'] = author
        item['text'] = clean_text
        item['translation'] = clean_translation
        item['comment'] = clean_comment

        yield item

        pass

