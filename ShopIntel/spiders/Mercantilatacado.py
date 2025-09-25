import scrapy
import json

from ShopIntel.items import ShopintelItem


class PrecoHunterSpider(scrapy.Spider):
    name = "Mercantilatacado"
    domains = "https://www.mercantilatacado.com.br"
    headers = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
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
            url="https://www.mercantilatacado.com.br/_v/private/graphql/v1?workspace=master&maxAge=long&appsEtag=remove&domain=store&locale=pt-BR",
            method="POST",
            body=json.dumps(payload),
            callback=self.store_data,
            headers=self.headers,
        )

    def store_data(self, response):
        data_json = response.json()

        for store in data_json["data"]["pickupPoints"]:
            data_stores = {
                "name": store["name"],
                "id_store": store["id"],
                "city": store["address"]["city"],
            }

        yield scrapy.Request(
            url="https://www.mercantilatacado.com.br/api/catalog_system/pub/category/tree/100",
            method="GET",
            callback=self.category,
        )

    def category(self, response):

        for data_json in response.json():

            data_category = {
                "id": data_json["id"],
                "name": data_json["name"],
                
            }
            yield from self.request_products(data_json["id"])

    def request_products(self, id,page=1):

        yield scrapy.Request(
            url=f"https://www.mercantilatacado.com.br/api/catalog_system/pub/products/search?fq=C:{id}&_from={page}&_to=15",
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
      
        for item in response.json():

            get_price = item["items"][0]["sellers"][0]["commertialOffer"]["Installments"]
            if "[{" in get_price:
                price = get_price[0]["Value"]
            else:
                price =  item["items"][0]["sellers"][0]["commertialOffer"]["Price"]
                if price == 0:
                    price = None

                
            data_products = {
                    "name": item["items"][0]["name"],
                    "brand": item["brand"],
                    "sku": item["items"][0]["itemId"],
                    "ean": item["items"][0]["ean"],
                    "price": price,
                    "pricefrom": item["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"],
                    "store": {
                        "name": self.name,
                    }
                
                }
            yield data_products
    

        yield from self.request_products(id, page + 1)


        