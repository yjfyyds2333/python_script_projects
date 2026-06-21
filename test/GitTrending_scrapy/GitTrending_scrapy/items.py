# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GittrendingScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    repo_name = scrapy.Field()
    repo_language = scrapy.Field()
    repo_star_total = scrapy.Field()
    repo_star_today_increase = scrapy.Field()
    repo_spider_date = scrapy.Field()
    repo_score = scrapy.Field()

    pass
