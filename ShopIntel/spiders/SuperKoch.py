import scrapy
import json


class PrecoHunterSpider(scrapy.Spider):
    name = "SuperKoch"
   
    domains = "https://www.superkoch.com.br/"

    headers = {
            
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }

  

    def start_requests(self):
        yield scrapy.Request(
            url=self.domains,
            method="GET",
            callback=self.category,
            headers=self.headers
        )

    def category(self, response):
        
        for links in response.xpath('//nav[@class="navigation"]/ul/li[contains(@class, "level0 nav")]/a/@href').getall():
        
            yield scrapy.Request(
                url=links,
                method="GET",
                callback=self.request_products,
                headers=self.headers
            )
    def request_products(self, response):
        for links_products in response.xpath('//div[@class="products wrapper grid products-grid"]/ol/li/div/a/@href').getall():

            yield scrapy.Request(
                url=links_products,
                method="GET",
                callback=self.products,
                headers=self.headers
            )
            
    def products(self, response):
        offer = None
     
        get_price = response.xpath('//div[@class="column main"]/div[@class="product-info-main"]').get()

        if "old-price" in get_price:
            price = response.xpath('//div[@class="column main"]/div[@class="product-info-main"]/div[@class="product-info-price"]/div/span[@class="old-price"]/span/span/span/text()').get()
            offer = response.xpath('//div[@class="column main"]/div[@class="product-info-main"]/div[@class="product-info-price"]/div/span[@class="special-price"]/span/span/span/text()').get()

        else:
            price = response.xpath('//div[@class="column main"]/div[@class="product-info-main"]/div[@class="product-info-price"]/div/span/span/span/text()').get()
           

        data_products = {
                "name": response.xpath('//div[@class="column main"]/div[@class="product-info-main"]/div/h1/span/text()').get(),
                "price": offer,
                "pricefrom": price

            }
        print(data_products)
