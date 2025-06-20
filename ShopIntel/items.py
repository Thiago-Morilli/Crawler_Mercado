import scrapy


class ShopintelItem(scrapy.Item):
    
    name = scrapy.Field()
    id = scrapy.Field()
    sku = scrapy.Field()
    price = scrapy.Field()
    pricefrom = scrapy.Field()
    ean = scrapy.Field()

