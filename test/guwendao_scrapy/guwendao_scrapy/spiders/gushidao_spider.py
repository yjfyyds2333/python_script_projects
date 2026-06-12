import scrapy
import requests
from guwendao_scrapy.items import GuwendaoScrapyItem

class GushidaoSpiderSpider(scrapy.Spider):
    name = "gushidao_spider"
    allowed_domains = ["guwendao.net"]
    start_urls = ["https://www.guwendao.net/shiwens/default.aspx?cstr=%e5%94%90%e4%bb%a3"]

    # name = "shuge_spider"
    # allowed_domains = ["shuge.org"]
    # start_urls = ["https://www.shuge.org/collections/"]

    def parse(self, response):

        items = response.xpath('//div[@class="cont"]')
        print(f'一共获取到{len(items)}张卡片')
        self.logger.info(f'当前UA:{response.request.headers.get("User-Agent")}')

        for i,card in enumerate(items):
            item = GuwendaoScrapyItem()

            print(f'开始爬取第{i+1}条数据')

            try:          
                item['title'] = card.xpath('.//div[2]/p[1]/a/b/text()').get('').strip()
                item['author'] = card.xpath('.//div[2]/p[@class="source"]/a[@target="_blank"]/img/@alt').get('').strip() or card.xpath('.//div[2]/p[@class="source"]/a[@target="_blank"]/text()').get('').strip()
                item['age'] = card.xpath('.//div[2]/p[@class="source"]/a[2]/text()').get('')
                content_list1 = card.xpath('.//div[2]/div[@class="contson"]/text()').getall() 
                content_list2 = card.xpath('.//div[2]/div[@class="contson"]//p/text()').getall()
                # content是多行，拼接成字符串
                all_list = content_list1 + content_list2
                item['content'] = ''.join([text.strip() for text in all_list])
            except Exception as e:
                print(f'出现问题:{e}')

            yield item

        next_btn = response.xpath('//div[@class="pagesright"]/a[@class="amore"]/@href').get()
        if next_btn:
            yield response.follow(next_btn,callback=self.parse)

        # ===============shuge_parse====================
        
        # items = response.xpath('//article[@class="main_color inner-entry"]')
        # print(f'一共获取到{len(items)}张卡片')
        # self.logger.info(f'当前UA:{response.request.headers.get("User-Agent")}')

        # for i,card in enumerate(items):
        #     item = GuwendaoScrapyItem()

        #     print(f'开始爬取第{i+1}条数据')

        #     try:          
        #         item['title'] = card.xpath('.//h3[@class="grid-entry-title entry-title "]/a/@title').get('')
        #         item['age'] = card.xpath('.//span[@class="blog-categories minor-meta"]/a[1]/text()').get('')
        #         item['category'] = card.xpath('.//span[@class="blog-categories minor-meta"]/a[3]/text()').get('').strip()
        #     except Exception as e:
        #         print(f'出现问题:{e}')

        #     yield item

        # next_btn = response.xpath('//nav[@class="pagination"]/a[@class="inactive next_page"]/@href').get()
        # if next_btn:
        #     yield response.follow(next_btn,callback=self.parse)

        pass
