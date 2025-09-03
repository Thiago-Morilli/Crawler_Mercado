import scrapy
import json
from ShopIntel.items import ShopintelItem


class PrecoHunterSpider(scrapy.Spider):
    name = "ExtraMercado"
   
    domains = "https://www.extramercado.com.br/"

    headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        } 
    

    
    def start_requests(self):

        yield scrapy.Request(
            url="https://api.vendas.gpa.digital/ex/v3/products/categories/ecom?storeId=483&split=&showSub=true",
            method="GET",
            callback=self.category,
            
        )

    def category(self, response):
        
        for data in response.json()["content"]:

            yield from self.request_product(data["uiLink"])
        

    def request_product(self, category, page=1):
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
            url="https://api.vendas.gpa.digital/ex/search/category-page",
            method="POST",
            headers=self.headers,
            body=json.dumps(payload),
            callback=self.products,
            meta= {
                "category": category,
                "page": page
            }
        )


    def products(self, response):
        
        meta = response.meta
        category = meta["category"]
        page = meta["page"]
        
        for item in response.json()["products"]:
            offer = None
            price = item["price"]
    

            if "priceFrom" in item:
                
                price_offer = item["priceFrom"]

                if price_offer != price:
                    offer = price_offer
  
                     
            product_data = {
                "id": item["id"],
                "name": item["name"],
                "sku": item["sku"],
                "brand": item["brand"],
                "price": price,
                "pricefrom": offer

            }

            

            print(product_data)
                

            next_page = response.json()["totalPages"]

            if page != next_page:
                yield from self.request_product(category, page+1)
                

