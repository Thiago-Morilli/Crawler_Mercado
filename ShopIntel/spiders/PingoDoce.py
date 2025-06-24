import scrapy

class PrecoHunterSpider(scrapy.Spider):
    name = "pingo_doce"
    domains = "https://mercadao.pt"
    headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36"}
    data_stores = {}
   

    def start_requests(self):
        yield scrapy.Request(
            url=f"{self.domains}/api/pickingLocations/nearby?deliveryType=DELIVERY",
            method="GET",
            callback=self.store_data,
            headers=self.headers
        )

    def store_data(self, response):
        for data in response.json():
            stores_id = data["_id"]
            
            self.data_stores[stores_id] = {     
                    "name": data["name"],
                    "streetName": data["streetName"],
                    "city": data["city"],
                    "zipCode": data["zipCode"],
                    "brandId": data["brandId"],
                    "catalogueId": data["catalogueId"],
                    "department": data["brand"]["department"]
                }
    
        yield from self.request_category()                

    def request_category(self):
  
        yield scrapy.Request(
                url=f"{self.domains}/api/catalogues/6107d28d72939a003ff6bf51/with-descendants",
                method="GET",
                callback=self.category,
                headers=self.headers
            )

    def category(self, response):
        data_json = response.json()
        category_id = data_json["tree"]
        for id in category_id:
            yield from self.request_products(id)
            
    def request_products(self, id, page=0):
        yield scrapy.Request(
            url=f"{self.domains}/api/catalogues/6107d28d72939a003ff6bf51/products/search?mainCategoriesIds=%5B%22{id}%22%5D&sort=%7B%22activePromotion%22:%22desc%22%7D&from={page}&size=100&esPreference=0.24913664298082105",
            method="GET",
            callback=self.products,
            headers=self.headers,
            meta={
                "page": page,
                "id": id
            }
    )

    def products(self, response):
        data_json = response.json()
        meta = response.meta
        page = meta["page"]
        id = meta["id"]
        
        for items in data_json["sections"]["null"]["products"]:

            fixed_value = items["_source"]["regularPrice"]
            promotional_value = items["_source"]["buyingPrice"]

            if promotional_value < fixed_value:
                promotion = promotional_value

            else:   
                promotion = None

            
            data_products= {
                "name": items["_source"]["firstName"],
                "price": fixed_value,
                "promotion": promotion,
                "eans": items["_source"]["eans"]
            }

            
           
        
            

        yield from self.request_products(id, page+100)
        