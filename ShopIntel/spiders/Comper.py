import scrapy
import json


class PrecoHunterSpider(scrapy.Spider):
    name = "Comper"
    domains = "https://www.comper.com.br"

    def start_requests(self):

        yield scrapy.Request(
            url="https://www.comper.com.br/api/catalog_system/pub/category/tree/3/",
            method="GET",
            callback=self.category,
        )

    def category(self, response):
        for data in response.json():
            data_category =  {
                "id": data["id"],   
                "name": data["name"],
            }
            yield from self.request_products(data_category["id"])

    def request_products(self, id,page=1):

        yield scrapy.Request(
            url=f"https://www.comper.com.br/api/catalog_system/pub/products/search?fq=C:/{1284}/&PageNumber={page}&_from=0_to=4",
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
        for data_json in response.json():
            data = {
                "name": data_json["items"][0]["name"],
                "sku": data_json["items"][0]["itemId"],
                "ean": data_json["items"][0]["ean"],
            }
            print(data) 

        yield from self.request_products(id, page+1)