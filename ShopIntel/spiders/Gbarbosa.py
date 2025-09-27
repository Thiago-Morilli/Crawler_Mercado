import scrapy
import json

from ShopIntel.items import ShopintelItem


class PrecoHunterSpider(scrapy.Spider):
    name = "Gbarbosa"
    domains = "https://www.gbarbosa.com.br"
    headers = {
    "content-type": "application/json",
}

    
    
    def start_requests(self):

        payload = {
            "operationName": "pickupPoints",
            "variables": {},
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "9f31c72c8075b183236329e5b605e1922bd06afbce9348296261f9ac357b30c1",
                    "provider": "prezunic.store-selector@1.x",
                    "sender": "prezunic.store-selector@1.x"
                }
            }
        }

            
        yield scrapy.Request(
            url="https://www.gbarbosa.com.br/_v/private/graphql/v1?workspace=master&maxAge=long&appsEtag=remove&domain=store&locale=pt-BR&__bindingId=926eec74-c803-4719-aaf4-5a244a67b7f3",
            method="POST",
            body=json.dumps(payload),
            callback=self.store_data,
            headers=self.headers,
        )

    def store_data(self, response):

        for data in response.json()["data"]["pickupPoints"]:
            data_stores = {
                "name": data["name"],
                "id_store": data["id"],
                "city": data["address"]["city"],    
                "postalcode": data["address"]["postalCode"],
                
            }

        yield scrapy.Request(
            url="https://www.gbarbosa.com.br/api/catalog_system/pub/category/tree/100",
            method="GET",
            callback=self.category,
            meta={
                "name": data_stores["name"],
            
                }
        )
            
        
    def category(self, response):

        meta = response.meta

        for data in response.json():
            data_category = {
                "id": data["id"],
                "name": data["name"],
                
            }

            yield from self.request_products(data_category["id"], meta={"name": meta["name"]})

    
    def request_products(self, id,page=1, meta={}):
           
        meta.update({
        "name": meta.get("name"),
        })

        yield scrapy.Request(
            url=f"https://www.gbarbosa.com.br/api/catalog_system/pub/products/search?fq=C:{id}&_from={page}&_to=49",
            method="GET",
            callback=self.products,
            meta={
                "page": page,
                "id": id,
                "name_store": meta
            }
        )   
    
    def products(self, response):
        meta = response.meta
        page = meta["page"]
        id = meta["id"] 
        name_store = meta["name_store"]

        for data in response.json():   

            data_products = {
                "id": data["productId"],
                "name": data["productName"],
                "price": data["items"][0]["sellers"][0]["commertialOffer"]["Price"],
                "pricefrom": data["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"],
                "sku": data["items"][0]["itemId"],
                "ean": data["items"][0]["ean"],
                "brand": data["brand"],
                "store": {
                    "name": self.name,
                
                }
            }


            yield data_products


        yield from self.request_products(id,page + 1)
      