import scrapy
import json

from ShopIntel.items import ShopintelItem


class PrecoHunterSpider(scrapy.Spider):
    name = "Carrefour"
    domains = "https://www.carrefour.es"
    search = "/supermercado"
    headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36",
        }
    
    def start_requests(self):
            
        yield scrapy.Request(
            url=self.domains + self.search,
            method="GET",
            callback=self.category,
            headers=self.headers
        )

    def category(self, response):

        for categories in response.xpath('//div[@class="nav-first-level-categories"]/div/a/@href').getall():
            yield scrapy.Request(
                        url=self.domains + categories,
                        method="GET",
                        callback=self.request_products,     
                        headers=self.headers                   
                    )
            
        
    def resquest_page(self, page):
       
        yield scrapy.Request(
            url=page,
            method="GET",
            callback=self.request_products,
            headers=self.headers
        )

    def request_products(self, response):
        
        for item in response.xpath('//ul[@class="product-card-list__list"]/li/div/div/div[@class="product-card__media"]/a/@href').getall():
            yield scrapy.Request(
                            url=self.domains + item,
                            method="GET",
                            callback=self.product,  
                            headers=self.headers                      
                 )
        
            yield from self.pagination(response)

    def product(self, response):
                
        path_json = response.xpath('//script[@type="application/ld+json"]/text()').get()
        json_info = json.loads(path_json)

        if json_info["@type"] == "Product":

            data_products = {
            "name": json_info["name"],
            "sku": json_info["sku"],
            "ean": json_info["gtin13"],
            "brand": json_info["brand"]["name"],
            "price": json_info["offers"]["price"],
            "store": {
                "name": self.name
            }
                
                    }

            yield data_products

    def pagination(self, response):
        page = response.xpath('//div[@class="pagination__row"]/a/@href').getall()
        
        if page != []:
            if len(page) == 1:
                yield from self.resquest_page(self.domains + page[0])

            elif len(page) == 2:
                yield from self.resquest_page(self.domains + page[1])
            
        