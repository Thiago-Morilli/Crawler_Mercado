import scrapy


class SaoRoqueSpider(scrapy.Spider):
    name = "pingo_doce"
    domains = "https://mercadao.pt"
    headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36"}
   


    def start_requests(self):
        yield scrapy.Request(
            url=f"{self.domains}/api/pickingLocations/nearby?deliveryType=DELIVERY",
            method="GET",
            callback=self.store_data,
            headers=self.headers
        )

    def store_data(self, response):
        for data_json in response.json():

            collecting_stores = {
                    "id": data_json["_id"],
                    "name": data_json["name"],
                    "streetName": data_json["streetName"],
                    "city": data_json["city"],
                    "zipCode": data_json["zipCode"]
                }
            
            yield scrapy.Request(
                url=f"{self.domains}/api/banners/getBanners?type=CATEGORY_HEADER&brand=59d39b29ef6ad4002836d627&pickingLocation=5b26e01679d664001ec65844&catalogueCategoryId=61eedde8fd2bff003f508138",
                method="GET",
                callback=self.category,
                headers=self.headers
            )


    def category(self, response):
        data_json = response.json()
        print(data_json)