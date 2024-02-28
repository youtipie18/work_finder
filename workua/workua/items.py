# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WorkuaItem(scrapy.Item):
    title = scrapy.Field()
    requirements = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
