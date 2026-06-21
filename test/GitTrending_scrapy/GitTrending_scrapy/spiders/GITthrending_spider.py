import scrapy
from datetime import date
import time,re
from GitTrending_scrapy.items import GittrendingScrapyItem


class GitthrendingSpiderSpider(scrapy.Spider):
    name = "GITthrending_spider"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/trending/python?since=daily",
                  "https://github.com/trending/javascript?since=daily",
                  "https://github.com/trending/go?since=daily",
                  "https://github.com/trending/java?since=daily",
                  "https://github.com/trending/rust?since=daily"
                ]

    def parse(self, response):

        cards = response.xpath('//article[@class="Box-row"]')
        print(f'一共获取到{len(cards)}个卡片')

        for card in cards:
            item = GittrendingScrapyItem()

            try:
                item['repo_name'] = card.xpath('.//h2[@class="h3 lh-condensed"]/a/text()[last()]').get('').strip()
                item['repo_language'] = card.xpath('.//span[@itemprop="programmingLanguage"]/text()').get('')
                item['repo_star_total'] = card.xpath('.//a[@class="tmp-mr-3 Link Link--muted d-inline-block"]/text()').get('').strip()
                item['repo_star_today_increase'] = card.xpath('.//span[@class="d-inline-block float-sm-right"]/text()[last()]').get('').strip()
                item['repo_spider_date'] = date.today()

            except Exception as e:
                print(f'爬取失败,错误原因:{e}')

            yield item

        pass
