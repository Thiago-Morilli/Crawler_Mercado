import scrapy
from MiniPreco.items import MiniprecoItem

class ProductsSpider(scrapy.Spider):
    name = "Products"
    domains = "https://www.minipreco.pt/"

    def start_requests(self):
        yield scrapy.Request(
            url=self.domains,
            method="GET",
            callback=self.category
        )

    def category(self, response):
        for category_link in response.xpath('//div[@class="category-link"]/a/@href').getall():
            yield scrapy.Request(
                url=self.domains + category_link,
                method="GET",
                callback=self.parse
            )
    
    def requests_page(self, link):
        yield scrapy.Request(
            url=link,
            method="GET",
            callback=self.parse
        )

    def parse(self, response):
        for product_links in response.xpath('//div[@class="prod_grid "]/a/@href').getall():
            yield scrapy.Request(
                url=self.domains + product_links,
                method="GET",
                callback=self.products,
                meta={
                    "link":self.domains + product_links
                }
            )
       
        yield from self.page(response)
       

    def products(self, response):
        meta = response.meta

        collecting_data = {
        "name": response.xpath('//div[@class="product-name"]/h1/text()').get(),
        "price": response .xpath('//div[@class="price-container"]/p/span/text()').get(),
        "kilo_price": response.xpath('//div[@class="price-container"]/span/text()').get (),
        "link": meta["link"]
        }

        yield MiniprecoItem(
            collecting_data
            )

    def page(self, response):
        next_page = response.xpath('//ul[@class="pager pagination-component"]/li[@class="next"]/a/@href').get()
        if next_page:
            if next_page != "#":
                link_page = self.domains + next_page
                yield from self.requests_page(link_page)
            else:
                print("Nao tem mais paginas")
        else:
            print("Link nao encontrado.")