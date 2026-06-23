# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FangtxScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    house_id = scrapy.Field()
    price_history = scrapy.Field()
    house_title =  scrapy.Field()
    house_total_price = scrapy.Field()
    house_unix_price= scrapy.Field()
    house_type = scrapy.Field()
    house_square = scrapy.Field()
    house_towards = scrapy.Field()
    house_floors= scrapy.Field()
    house_community = scrapy.Field()
    house_area = scrapy.Field()

    pass
