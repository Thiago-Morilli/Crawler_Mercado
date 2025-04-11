import scrapy
from Froiz.items import FroizItem


class ProductsSpider(scrapy.Spider):
    name = "Products"
    domains = "https://loja.froiz.com/"
    data = {}

    def start_requests(self):
        yield scrapy.Request(
            url=self.domains,
            method="GET",
            callback=self.first_category
        )

    def first_category(self, response):
        for link_category in response.xpath('//div[@class="span3"]/ul[@class="nav nav-pills nav-stacked"]/li/a/@href').getall():
            yield scrapy.Request(
                url=self.domains + link_category,
                method="GET",
                callback=self.second_category
            )


    def second_category(self, response):
        for link_category in response.xpath('//div[@class="span3"]/div/div[@class="accordion-body collapse"]/div/ul/li/a/@href').getall():
            yield scrapy.Request(
                url=self.domains + link_category,
                method="GET",
                callback=self.products

            )

    def products(self, response):
        for link_product in response.xpath('//div[@class="product"]/div/div/a/@href').getall():
            yield scrapy.Request(
                url=self.domains + link_product,
                method="GET",
                callback=self.collecting_data
            )

    def collecting_data(self, response):
    
        self.data["name"] = response.xpath('//div[@class="span7"]/div[@class="product-title"]/h3/text()').get()
        self.data["price"] = response.xpath('//div[@class="span7"]/div[@class="product-title"]/div[@class="meta"]/span/text()').get()
        self.data["kilogram_price"] = response.xpath('//div[@class="span7"]/div[@style="float: left"]/div/span/text()').get()
        promotional_price = response.xpath('//div[@class="span7"]/div[@class="product-title"]/div[@class="meta"]/span[@class="tag red-clr"]/text()').get()
        if promotional_price != None:
            self.data["promotional_price"] = promotional_price
            self.data["price"] = response.xpath('//div[@class="span7"]/div[@class="product-title"]/div[@class="meta"]/span[@class="tag striked"]/small/text()').get().strip()
        else:
            self.data["promotional_price"] = "Não tem promoçao."
        
        
        yield FroizItem(
            self.data
        )



    
