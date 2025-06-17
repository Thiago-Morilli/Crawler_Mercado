import scrapy
import json


class PrecoHunterSpider(scrapy.Spider):
    name = "Muffato"
   
    domains = "https://www.supermuffato.com.br/"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.supermuffato.com.br/api/catalog_system/pub/category/tree/4",
            method="GET",
            callback=self.category
        )

    def category(self, response):
        print(response.json())
       