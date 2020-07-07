# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    pass


class a91Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    img = scrapy.Field()
    add_time = scrapy.Field()
    author = scrapy.Field()
    views = scrapy.Field()
    favorite = scrapy.Field()
    collection = scrapy.Field()
    msg = scrapy.Field()
    score = scrapy.Field()
    time = scrapy.Field()
    create_time = scrapy.Field()
    video_url=scrapy.Field()
