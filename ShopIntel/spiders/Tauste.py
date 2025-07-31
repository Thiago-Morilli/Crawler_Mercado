import scrapy
from ShopIntel.items import ShopintelItem



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
            
    def request_page(self, page):
        yield scrapy.Request(
            url=page,
            method="GET",
            callback=self.request_products,
            headers=self.headers
        )
            
    def request_products(self, response):
        for items in response.xpath('//ol[@class="products list items product-items"]/li/div/a/@href').getall():
            yield scrapy.Request(
                url=items,
                method="GET",
                callback=self.product,
                headers=self.headers
            )

        yield from self.pagination(response)

    def product(self, response):
            
        data_product = {
            "name": response.xpath('//div[@class="product-info-main"]/div/h1/span/text()').get(),
            "sku": response.xpath('//div[@class="product attribute sku"]/div/text()').get(),
            "price": response.xpath('//div[@class="price-box price-final_price"]/span/span/span/text()').get().replace("R$", "").strip(),
        }
            
        yield ShopintelItem(data_product)

    def pagination(self, response):
        page = response.xpath('//div[@class="pages"]/ul/li[@class="item pages-item-next"]/a/@href').get()
        if page:
          
            yield from self.request_page(page)