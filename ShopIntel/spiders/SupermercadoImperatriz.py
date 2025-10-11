import scrapy
import json

from ShopIntel.items import ShopintelItem


class PrecoHunterSpider(scrapy.Spider):
    name = "SupermercadoImperatriz"
    domains = "https://www.supermercadosimperatriz.com.br"

    def start_requests(self):

            
        yield scrapy.Request(
            url="https://www.supermercadosimperatriz.com.br/api/catalog_system/pub/category/tree/2/",
            method="GET",
            callback=self.category,
        )

    def category(self, response):
        for data_json in response.json():
            data_category = {
                "id": data_json["id"],
                "name": data_json["name"],
            }
            yield from self.request_products(data_category["id"])
 
    def request_products(self, id, page=1):

        yield scrapy.Request(
            url=f"https://www.supermercadosimperatriz.com.br/api/catalog_system/pub/products/search?fq=C:/{id}/&PageNumber={page}&_from=0&_to=4",
            method="GET",
            callback=self.products,
            meta={
                "page": page,
                "id": id
            }
        )

    def products(self, response):
        meta = response.meta
        page = meta["page"]
        id = meta["id"]
        for data in response.json():

 
            price = data["items"][0]["sellers"][0]["commertialOffer"]["Price"]
            get_pricefrom = data["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]
            if get_pricefrom > price:
                pricefrom = get_pricefrom
            else:
                pricefrom = None

            ean = data["items"][0]["ean"]
            if ean == '':
                ean = None
            else:
                if ',' in ean:
                    ean = ean.replace(',', '')
                else:
                    ean = ean

            data_products = {   
                "sku": data["items"][0]["itemId"],
                "name": data["items"][0]["name"],
                "brand": data["brand"],
                "ean": ean,
                "price": price,
                "pricefrom": pricefrom,
                "store": {
                    "name": self.name,
                }
            }

            yield data_products    

        yield from self.request_products(id, page+1)