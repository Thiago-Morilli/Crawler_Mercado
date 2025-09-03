
import scrapy

class PrecoHunterSpider(scrapy.Spider):
    name = "Palato"
   
    domains = "https://loja.palato.com.br/"

    def start_requests(self):

        yield scrapy.Request(
            url=self.domains,
            method="GET",
            callback=self.category,
           
            
        )

    def category(self, response):
        for categories in response.xpath('//ul[@class="menu-section"]/li[position() = 1]/div/div/a/@href').getall():
            yield scrapy.Request(
                        url=categories,
                        method="GET",
                        callback=self.request_products,                        
                    )
            
    def request_page(self, page):
        yield scrapy.Request(
            url=page,
            method="GET",
            callback=self.request_products,
            
        )

    def request_products(self, response):
        for items in response.xpath('//div[@class="card-product-filter d-flex flex-wrap"]/div/div/div[@class="item-image product"]/a/@href').getall():
           yield scrapy.Request(
                        url=items,
                        method="GET",
                        callback=self.product,                        
                    )
        yield from self.pagination(response)
    def product(self, response):  
            price_raw = response.xpath('//div[@class="row"]/div[@class="col-lg-6 col-md-12 col-12 order-2"]/div[@class="product-info"]/div[@class="prices-discount"]/div[@class="pricesGeneral"]/h2/span/text()').get()
            if price_raw != None:
                price = price_raw.replace("R$", "").strip()
            else:
                price = response.xpath('//div[@class="row"]/div[@class="col-lg-6 col-md-12 col-12 order-2"]/div[@class="product-info"]/div[@class="prices-discount"]/div[@class="pricesGeneral"]/div/span/text()').get().replace("R$", "").strip()

            pricefrom = response.xpath('//div[@class="row"]/div[@class="col-lg-6 col-md-12 col-12 order-2"]/div[@class="product-info"]/div[@class="prices-discount"]/div/div/span[@class="price"]/text()').get()
            if pricefrom:  
                pricefrom = pricefrom.replace("R$", "").strip()
                    
                if pricefrom > price:
                    offer = pricefrom 
                    
            else:
                offer = None

            data_product = {
                    "name": response.xpath('//div[@class="row"]/div[@class="col-lg-6 col-md-12 col-12 order-2"]/h1/text()').get(),
                    "sku": response.xpath('//div[@class="row"]/div[@class="col-lg-6 col-md-12 col-12 order-2"]/div[@class="product-info"]/div/span/text()').getall()[1].replace("\n", "").strip(),
                    "price": price,
                    "pricefrom": offer
                 }
            
    def pagination(self, response):
        page = response.xpath('//nav[@aria-label="Page navigation example"]/ul/li[@title="Próxima"]/a/@href').get()
        if page:
            yield from self.request_page(page)
