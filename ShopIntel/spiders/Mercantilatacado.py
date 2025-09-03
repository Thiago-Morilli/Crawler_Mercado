import scrapy
import json

from ShopIntel.items import ShopintelItem
#https://www.mercantilatacado.com.br/_v/private/graphql/v1?workspace=master&maxAge=long&appsEtag=remove&domain=store&locale=pt-BR


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
        print(response)

        '''yield scrapy.Request(
            url="""https://www.mercantilatacado.com.br/_v/segment/graphql/v1?workspace=master&maxAge=medium&appsEtag=remove&domain=store&locale=pt-BR&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%221e74d3c82905026a7279010d9ac02c0419cb26a788cd5cb0c56045eb5b450edc%22%2C%22sender%22%3A%22mercantilatacado.category-seo%400.x%22%2C%22provider%22%3A%22vtex.store-graphql%402.x%22%7D%7D""",
            method="GET",
            callback=self.category,
        )'''

    def category(self, response):
       pass