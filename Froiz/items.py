import scrapy


class FroizItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    kilogram_price = scrapy.Field()
    promotional_price = scrapy.Field()