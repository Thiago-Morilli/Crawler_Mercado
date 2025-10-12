import scrapy
import json

from ShopIntel.items import ShopintelItem


class PrecoHunterSpider(scrapy.Spider):
    name = "Shibata"
    domains = "https://www.loja.shibata.com.br/home"
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    headers = {
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJ2aXBjb21tZXJjZSIsImF1ZCI6ImFwaS1hZG1pbiIsInN1YiI6IjZiYzQ4NjdlLWRjYTktMTFlOS04NzQyLTAyMGQ3OTM1OWNhMCIsInZpcGNvbW1lcmNlQ2xpZW50ZUlkIjpudWxsLCJpYXQiOjE3NTg5NzM4OTQsInZlciI6MSwiY2xpZW50IjpudWxsLCJvcGVyYXRvciI6bnVsbCwib3JnIjoiMTYxIn0.0vTxzHy1vdj7VfG5oHtLWLbjm5r9RxSkJJuuVNy1QigU61_yaH9MPmv84jqdoFdXQs4vRatPrshFrvjMPE0FtA",
    "content-type": "application/json",
    "domainkey": "loja.shibata.com.br",
    "organizationid": "161",
   
 }
 
    def start_requests(self):

            
        yield scrapy.Request(
            url="https://services.vipcommerce.com.br/api-admin/v1/org/161/filial/1/centro_distribuicao/1/loja/classificacoes_mercadologicas/departamentos/arvore",
            method="GET",
            callback=self.category,
            headers=self.headers,
        )

    def category(self, response):

        for data in response.json()['data']:
            data_category =  {
                "id": data["classificacao_mercadologica_id"],
                "name": data["descricao"],
            }

    
            yield from self.request_products(data_category["id"])

    def request_products(self, id,page=1):
        yield scrapy.Request(
            url="https://services.vipcommerce.com.br/api-admin/v1/org/161/filial/1/centro_distribuicao/29/loja/classificacoes_mercadologicas/departamentos/1/produtos?page=1&",
            method="GET",
            callback=self.products,
            headers=self.headers,
        )
    
    def products(self, response):
        pass


