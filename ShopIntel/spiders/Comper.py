import scrapy
import json


class PrecoHunterSpider(scrapy.Spider):
    name = "Comper"
    domains = "https://www.comper.com.br"

    def start_requests(self):

        yield scrapy.Request(
            url="https://www.comper.com.br/api/catalog_system/pub/category/tree/3/",
            method="GET",
            callback=self.category,
        )

    def category(self, response):
        for data in response.json():
            data_category =  {
                "id": data["id"],   
                "name": data["name"],
            }
            yield from self.request_products(data_category["id"])

    def request_products(self, id,page=1):

        yield scrapy.Request(
            url="https://www.comper.com.br/api/catalog_system/pub/products/search?fq=C:/1281/&PageNumber=1&_from=50&_to=99",
            method="GET",
            callback=self.products,
        )
    
    def products(self, response):
        print(response) 