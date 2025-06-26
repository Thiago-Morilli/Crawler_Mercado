import scrapy
import json


class PrecoHunterSpider(scrapy.Spider):
    name = "PaodeAcucar"
   
    domains = "https://www.paodeacucar.com"

    def start_requests(self):
        yield scrapy.Request(
            url="https://api.vendas.gpa.digital/pa/catalog-page/5fbdb64d399df472afbc6b9c/461",
            method="GET",
            callback=self.id_category
            
        )

    def id_category(self, response):
        id = response.json()["deliveryFrom"]
        
        yield scrapy.Request(
            url=f"https://api.vendas.gpa.digital/pa/v3/products/categories/ecom?storeId={id}&split=&showSub=true",
            method="GET",
            callback=self.category
        )
    
    def category(self, response):

        for data in response.json()["content"]:
            
            yield from self.request_product(data["uiLink"])

    def request_product(self, category, page=1):
            
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
            } 

            payload = {
                "partner": "linx",
                "page": page,
                "resultsPerPage": 12,
                "multiCategory": "alimentos",
                "department": "ecom",
                "customerPlus": True,
                "sortBy": "relevance",
                "storeId": 461
                }
            
            yield scrapy.Request(
                url="https://api.vendas.gpa.digital/pa/search/category-page",
                method="POST",
                headers=headers,
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
       

        for items in response.json()["products"]:
            offer = None
            price = items["price"]
            
            if "priceFrom" in items:
                price_offer = items["priceFrom"]
                
                if price != price_offer:
                    offer = price_offer

            if "brand" in items:
                brand = items["brand"]
            else:
                brand = None    


            product_data = {
                "name": items["name"],
                "id": items["id"],
                "sku": items["sku"],
                "brand": brand,
                "price": price,
                "pricefrom": offer
            }
      
        next_page = response.json()["totalPages"]
        if page != next_page:

            yield from self.request_product(category, page + 1) 
       
         
