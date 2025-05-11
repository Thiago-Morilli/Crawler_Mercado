import scrapy


class SaoRoqueSpider(scrapy.Spider):
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
            data_category = {
                        "name": data_json["tree"][id]["name"] 
            }
          
        