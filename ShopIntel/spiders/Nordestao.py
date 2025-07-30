
import scrapy
import json



class PrecoHunterSpider(scrapy.Spider):
    name = "Nordestao"
   
    domains = "https://www.lojaonline.nordestao.com.br/"

    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

 

    headers = {
            "accept": "application/json",
            "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJ2aXBjb21tZXJjZSIsImF1ZCI6ImFwaS1hZG1pbiIsInN1YiI6IjZiYzQ4NjdlLWRjYTktMTFlOS04NzQyLTAyMGQ3OTM1OWNhMCIsInZpcGNvbW1lcmNlQ2xpZW50ZUlkIjpudWxsLCJpYXQiOjE3NDg5NzgxMDksInZlciI6MSwiY2xpZW50IjpudWxsLCJvcGVyYXRvciI6bnVsbCwib3JnIjoiNTIifQ.wnrWB1s41oatsLOxkjAu2TFha8cSEDJZfY7y-WiaA1aNVk9E1C0et96FSnzDNTtLRQ-hYA33O6AksFQwzDGpcw",
            "content-type": "application/json",
            "domainkey": "nordestaomaisvoce.com.br",
            "organizationid": "52",
            "origin": "https://www.lojaonline.nordestao.com.br",
            "referer": "https://www.lojaonline.nordestao.com.br/",
            "sessao-id": "bafc404c30bba9c78874ef0c5c4842f9",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36",

        }

    
    def start_requests(self):

        yield scrapy.Request(
            url="https://services.se1.vipcommerce.com.br/api-admin/v1/org/52/filial/1/centro_distribuicao/4/loja/classificacoes_mercadologicas/departamentos/arvore",
            method="GET",
            callback=self.category,
            headers=self.headers,
            
        )

    def category(self, response):
        data_json = response.json()
        for category_id in data_json['data']:
            id = category_id['classificacao_mercadologica_id']

            yield from self.request_products(id)

    def request_products(self, id, page=0):
        yield scrapy.Request(
            url=f"https://services.se1.vipcommerce.com.br/api-admin/v1/org/52/filial/1/centro_distribuicao/4/loja/classificacoes_mercadologicas/departamentos/{id}/produtos?page={page}&",
            method="GET",
            callback=self.products,
            headers=self.headers,
            meta={
                "page": page,
                "id": id
            }
        )
    def products(self, response):
        for data_json in response.json()["data"]:
            price = data_json["preco"]
            special_price = data_json["oferta"]

            if special_price:
                price_offer = special_price["preco_oferta"]

                if price > price_offer:
                    offer = price_offer
            else:
                offer = None

            data_product = {
                "name": data_json["descricao"],
                "ean": data_json["codigo_barras"],
                "sku": data_json["sku"],
                "price": price,
                "pricefrom": offer
            }
            print(data_product) 