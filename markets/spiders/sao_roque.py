import scrapy


class SaoRoqueSpider(scrapy.Spider):
    name = "sao_roque"
    domains = "https://supersaoroque.com.br"
    store_dict = {}

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
        yield scrapy.Request(
            url=f"{self.domains}/maxipos_rest/rest/depto/loja/42?nocache=1746648173568",
            method="GET",
            callback=self.category
        )


    def category(self, response):
        data_json = response.json() 
        for data in data_json["deptos"]:
            category_id = data["codigo"]
            print(category_id)

    def parse(self, response):
        pass
