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
            url="""https://www.mercantilatacado.com.br/_v/segment/graphql/v1?workspace=master&maxAge=medium&appsEtag=remove&domain=store&locale=pt-BR&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%221e74d3c82905026a7279010d9ac02c0419cb26a788cd5cb0c56045eb5b450edc%22%2C%22sender%22%3A%22mercantilatacado.category-seo%400.x%22%2C%22provider%22%3A%22vtex.store-graphql%402.x%22%7D%7D""",
            method="GET",
            callback=self.category,
        )

    def category(self, response):

        for data_json in response.json()["data"]["categories"]:

            data_category = {
                "id": data_json["id"],
                "name": data_json["name"],
              
            }

        yield scrapy.Request(
            url="https://www.mercantilatacado.com.br/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR&operationName=Products&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22df92a25bd3b66d0bedddc38c8ed929c9c1242c041270c4128858582bd82cb29f%22%2C%22sender%22%3A%22vtex.store-resources%400.x%22%2C%22provider%22%3A%22vtex.search-graphql%400.x%22%7D%2C%22variables%22%3A%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6ZmFsc2UsInNrdXNGaWx0ZXIiOiJBTExfQVZBSUxBQkxFIiwiaW5zdGFsbG1lbnRDcml0ZXJpYSI6Ik1BWF9XSVRIT1VUX0lOVEVSRVNUIiwiY2F0ZWdvcnkiOiIyIiwic3BlY2lmaWNhdGlvbkZpbHRlcnMiOltdLCJvcmRlckJ5IjoiT3JkZXJCeUJlc3REaXNjb3VudERFU0MiLCJmcm9tIjowLCJ0byI6OSwic2hpcHBpbmdPcHRpb25zIjpbXSwidmFyaWFudCI6IiIsImFkdmVydGlzZW1lbnRPcHRpb25zIjp7InNob3dTcG9uc29yZWQiOmZhbHNlLCJzcG9uc29yZWRDb3VudCI6MiwicmVwZWF0U3BvbnNvcmVkUHJvZHVjdHMiOmZhbHNlLCJhZHZlcnRpc2VtZW50UGxhY2VtZW50IjoiaG9tZV9zaGVsZiJ9fQ%3D%3D%22%7D",
            method="GET",
            callback=self.products,
        )
    
    def products(self, response):

        for item in response.json()["data"]["products"]:

                
            data_products = {
                    "name": item["productName"],
                    "sku": item["items"][0]["itemId"],
                    "ean": item["items"][0]["ean"],
                
                }
            print(data_products)


        