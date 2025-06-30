import scrapy
import json



class PrecoHunterSpider(scrapy.Spider):
    name = "SuperNosso"
   
    domains = "https://www.supernosso.com/"

    search = "produtos"
    
    def start_requests(self):

        yield scrapy.Request(
            url=self.domains,
            method="GET",
            callback=self.category,
            
        )

    def category(self, response):
        for categories in response.xpath('//ul[@class="supernossoio-category-menu-2-x-sidebarContent pb7 list ma0 pa0"]/li/ul/li/a/@href').getall():
            yield scrapy.Request(
                url=categories,
                method="GET",
                callback=self.request_products,           
            )

    def request_products(self, response):

        for items in response.xpath('//div[@class="vtex-search-result-3-x-gallery flex flex-row flex-wrap items-stretch bn ph1 na4 pl9-l"]/div/section/a/@href').getall():
            yield scrapy.Request(
                url=self.domains + items,
                method="GET",
                callback=self.products,
             
            )

    def products(self, response):

        path_json = response.xpath('//script[@type="application/ld+json"]/text()').get()
        json_info = json.loads(path_json)

        data = {
            "name": json_info["name"],
        }
        
       # data = response.json()

        print(data )
        

















        