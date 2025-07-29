import scrapy
import json



class PrecoHunterSpider(scrapy.Spider):
    name = "Angeloni"
   
    domains = "https://www.angeloni.com.br/"

    search = "super/"

    headers = {
            
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }

    
    def start_requests(self):

        yield scrapy.Request(
            url=self.domains + self.search,
            method="GET",
            callback=self.category,
            headers=self.headers,
            
        )

    def category(self, response):

  
        for categories in response.xpath('//div[@class="superangeloni-main-menu-0-x-mainMenuWrapperCategory"]/h4[@class="flex superangeloni-main-menu-0-x-mainMenuWrapperCategoryContent superangeloni-main-menu-0-x-mainMenuWrapperCategoryContentItems"]/a/@href').getall():
            
            yield scrapy.Request(
                    url=self.domains + categories,
                    method="GET",
                    callback=self.request_products,
                    headers=self.headers
                )

    def request_products(self, response):
               # itmes = response.xpath()

                print(response)

    