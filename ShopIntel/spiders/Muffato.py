import scrapy
import json


class PrecoHunterSpider(scrapy.Spider):
    name = "Muffato"
   
    domains = "https://www.supermuffato.com.br/"

    ids_category = [144, 146, 151, 145, 148, 150, 154, 147, 149, 152, 153]

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.supermuffato.com.br/api/catalog_system/pub/category/tree/4",
            method="GET",
            callback=self.category
        )

    def category(self, response):
        print(response.json()[0])
       