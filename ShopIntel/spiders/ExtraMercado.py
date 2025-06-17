import scrapy
import json


class PrecoHunterSpider(scrapy.Spider):
    name = "ExtraMercado"
   
    domains = "https://www.extramercado.com.br/"

    headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        } 

    
    def start_requests(self, page=1):
        payload = {
                "partner": "linx",
                "page": page,
                "resultsPerPage": 12,
                "multiCategory": "alimentos",
                "sortBy": "relevance",
                "storeId": 483,
                "customerPlus": True,
                "department": "ecom"
            }

        yield scrapy.Request(
            url="https://api.vendas.gpa.digital/ex/v3/products/categories/ecom?storeId=483&split=&showSub=true",
            method="GET",
            callback=self.category,
            meta = {
                "payload": payload,
                "page": page
            }
        )


    def category(self, response):
        meta = response.meta
        payload = meta["payload"]
        page = meta["page"]
    
       
        for data in response.json()["content"]:

            data_category = {
                "link": data["uiLink"],
                "id": data["id"]
            }

        yield scrapy.Request(
            url="https://api.vendas.gpa.digital/ex/search/category-page",
            method="POST",
            headers=self.headers,
            body=json.dumps(payload),
            callback=self.products,
            meta= {
                "payload": payload,
                "page": page
            }
        )

    def products(self, response):
        meta = response.meta
        page = meta["page"]
        
        for item in response.json()["products"]:
            offer = None
            price = item["price"]

            if "productPromotions" in item:
                for Promotions in item["productPromotions"]:
                    price = Promotions["unitPrice"]

                pricefrom = item["price"]

                if price < pricefrom:
                    offer = pricefrom
                
                
            product_data = {
                "id": item["id"],
                "name": item["name"],
                "sku": item["sku"],
                "price": price,
                "pricefrom": offer

            }
        yield from self.start_requests(page+1)

