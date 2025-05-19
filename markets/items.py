
import scrapy


class SaoRoque02Item(scrapy.Item): 
    name = scrapy.Field()
    code = scrapy.Field()
    ean = scrapy.Field()
    price = scrapy.Field()
    promotion = scrapy.Field()
    
