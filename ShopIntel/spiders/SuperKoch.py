import scrapy
from ShopIntel.items import ShopintelItem


class PrecoHunterSpider(scrapy.Spider):
    name = "SuperKoch"
    domains = "https://www.superkoch.com.br/"
    headers = {
            
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }

    def start_requests(self):
        yield scrapy.Request(
            url=self.domains,
            method="GET",
            callback=self.category,
            headers=self.headers
        )

    def category(self, response):
        
        for links in response.xpath('//nav[@class="navigation"]/ul/li[contains(@class, "level0 nav")]/a/@href').getall():
        
            yield scrapy.Request(
                url=links,
                method="GET",
                callback=self.request_products,
                headers=self.headers
            )

    def request_page(self, page):

        yield scrapy.Request(
            url=page,
            method="GET",
            callback=self.request_products,
            headers=self.headers
        )

    def request_products(self, response):
        for links_products in response.xpath('//div[@class="products wrapper grid products-grid"]/ol/li/div/a/@href').getall():

            yield scrapy.Request(
                url=links_products,
                method="GET",
                callback=self.products,
                headers=self.headers
            )
            
        yield from self.next_page(response)

    def products(self, response):
        offer = None
        get_price = response.xpath('//div[@class="column main"]/div[@class="product-info-main"]').get()
        
        if "old-price" in get_price:
            offer = response.xpath('//div[@class="column main"]/div[@class="product-info-main"]/div[@class="product-info-price"]/div/span[@class="old-price"]/span/span/span/text()').get().replace("R$\xa0", "").replace(",",".")
           
            special_price = response.xpath('//div[@class="column main"]/div[@class="product-info-main"]/div[@class="product-info-price"]/div/span[@class="special-price"]/span/span/span/text()').get().replace("R$\xa0", "")
            

            if offer != special_price:
                price = special_price
                
                
        else:
            price = response.xpath('//div[@class="column main"]/div[@class="product-info-main"]/div[@class="product-info-price"]/div/span/span/span/text()').get().replace("R$\xa0", "")
        
        cont = 0
        for ean in  response.xpath('//div[@class="additional-attributes-wrapper table-wrapper"]/table/tbody/tr').getall():
            cont +=1
            if cont == 4:
                for ean in response.xpath('//td[contains(@data-th, "Ean")]/text()').getall():
                    break
            else:
                ean = None

        id = None
        data_products = {
                "name": response.xpath('//div[@class="column main"]/div[@class="product-info-main"]/div/h1/span/text()').get(),
                "price": price.replace(",","."),
                "pricefrom": offer,
                "sku": response.xpath('//div[@class="column main"]/div[@class="product-info-main"]/div[@class="product-info-price"]/div[@class="product-info-stock-sku"]/div[@class="product attribute sku"]/div/text()').get(),
                "ean": ean,
                "id": id
            }
        
        yield ShopintelItem(
            data_products
        )

    def next_page(self, response):
        page = response.xpath('//div[@class="pages"]/ul/li[@class="item pages-item-next "]/a/@href').get()
       
        if page:
            yield from self.request_page(page)

