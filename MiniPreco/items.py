import scrapy


class MiniprecoItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    kilo_price = scrapy.Field()
    link = scrapy.Field()
   