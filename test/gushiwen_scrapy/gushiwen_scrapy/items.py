# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GushiwenScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    poem_id = scrapy.Field()
    title = scrapy.Field()
    dynasty = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
    translation = scrapy.Field()
    comment = scrapy.Field()

    # 关键:字段名必须叫 file_urls（复数）,FilesPipeline只认这个名
    file_urls = scrapy.Field()
    # 下载结果会自动填充到files字段

    pass
