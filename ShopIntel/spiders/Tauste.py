import scrapy
import json



class PrecoHunterSpider(scrapy.Spider):
    name = "Tauste"
   
    domains = "https://tauste.com.br/"

    search = "marilia/"

    headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def start_requests(self):

        yield scrapy.Request(
            url=self.domains + self.search,
            method="GET",
            callback=self.category,
            headers=self.headers,
            
        )

    def category(self, response):

       for categories in response.xpath('//nav[@class="navigation"]/ul/li/a/@href').getall():
            yield scrapy.Request(
                    url=categories,
                    method="GET",
                    callback=self.request_products,
                    headers=self.headers
                )
            
    def request_products(self, response):
        print(response)
