import scrapy
from ShopIntel.items import ShopintelItem


class PrecoHunterSpider(scrapy.Spider):
    name = "SaoRoque"
    domains = "https://supersaoroque.com.br"
    store_dict = {}
    list_id = []

    def start_requests(self):
        yield scrapy.Request(
            url=f"{self.domains}/maxipos_rest/rest/loja/retira/0/0/?nocache=1746646460075",
            method="GET",
            callback=self.store_data
        )

    def store_data(self, response):
        data_json = response.json()
                
        for data in data_json:
            store_id = data["codigo"]
            self.store_dict[store_id] = {
                "name": data["nome"],
                "address": data["endereco"],    
                "neighborhood": data["bairro"],     
                "city": data["cidade"],
                "uf": data["uf"],
                "cep": data["cep"]
            }   
            self.list_id.append(store_id
                                )
        yield scrapy.Request(
            url=f"{self.domains}/maxipos_rest/rest/depto/loja/42?nocache=1746648173568",
            method="GET",       
            callback=self.category
        )


    def category(self, response):
      
        for store_id in self.list_id:
            data_json = response.json() 

            for data in data_json["deptos"]:
                category_id = data["codigo"]
                
                yield from self.request_products(store_id, category_id)

    def request_products(self, store_id, category_id, page=1):
        yield scrapy.Request(
            url=f"{self.domains}/maxipos_rest/rest/produto?p={page}&l=60&lj={store_id}&t=1&n1={category_id}&nocache=1746650469488",
            method="GET",
            callback=self.products,
            meta={
                "page": page,
                "category": category_id
            }
        )

    def products(self, response):
                                   
        data_json = response.json()
        meta = response.meta
        page = meta["page"]
        category_id = meta["category"]

        offer = None
        for items in data_json["produtos"]:
            stock = items["indisponivel"]
            if stock == 1:
                continue
            
            price = items["preco"]

            precode = items["precode"]

            if precode != 0.0:
                price = precode

                if price != precode:
                    offer = precode

            data_products = {
                "name": items["descricao"],
                "id": items["codigo"],
                "ean": items["ean"],
                "price": price,
                "pricefrom": offer
            }
          
            yield ShopintelItem(
                data_products
            )
         

        for store_id in self.list_id:
            if data_json != []:
                yield from self.request_products(store_id, category_id, page+1)