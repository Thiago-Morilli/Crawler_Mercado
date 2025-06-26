import scrapy
import json


class PrecoHunterSpider(scrapy.Spider):
    name = "Muffato"
   
    domains = "https://www.supermuffato.com.br/"

    def start_requests(self):
        yield scrapy.Request(
            url=self.domains,
            method="GET",
            callback=self.category
        )

    def category(self, response):

        categoria = response.xpath('//div[@class="muffatosupermercados-store-theme-0-x-drawerContent overflow-y-auto"]')
        print(categoria)
       