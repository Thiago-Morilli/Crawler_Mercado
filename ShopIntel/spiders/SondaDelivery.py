import scrapy
import json
from ShopIntel.items import ShopintelItem

class PrecoHunterSpider(scrapy.Spider):
    name = "SondaDelivery"
   
    domains = "https://www.sondadelivery.com.br/"

    def start_requests(self):
        yield scrapy.Request(
            url=self.domains,
            method="GET",
            callback=self.category
        )

    def category(self, response):
        for menus in  response.xpath('//ul[@class="nav navbar-nav"]/li[@class="section-menu"]/div/div/ul/li/a/@href').getall():
            yield scrapy.Request(
                url=self.domains+menus,
                method="GET",
                callback=self.products

            )
    def request_page(self, link):
        yield scrapy.Request(
            url=self.domains+link,
            method="GET",
            callback=self.products
        )

    def products(self, response):
        for items in response.xpath('//div[@class="row product-list"]/div[@class="col-xs-12 col-md-8"]/div/figure/a/@href').getall():
            yield scrapy.Request(
                url=self.domains+items,
                method="GET",
                callback=self.collecting_data
            )

        yield from self.pagination(response)

    def collecting_data(self, response):
        path_json = response.xpath('//script[@type="application/ld+json"]/text()').get()
        json_info = json.loads(path_json)

        data = {
            "name": json_info["name"],
            "sku": json_info["sku"],
            "price": json_info["offers"]["price"]
        }

        yield ShopintelItem(
            data
        )

    def pagination(self, response):

        page = response.xpath('//div[@class="input-qtd"]/div[@id="ctl00_conteudo_pnlPaginaProximaRodape"]/a/@href').get()

        if page != None:
            
            yield from self.request_page(page)

  