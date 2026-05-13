import scrapy


class PrecoHunterSpider(scrapy.Spider):
    name = "Angeloni"
    domains = "https://www.angeloni.com.br"
    search = "/super/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def start_requests(self):
        yield scrapy.Request(
            url=self.domains + self.search,
            method="GET",
            callback=self.category,
            # headers=self.headers,
        )

    def category(self, response):
        for category in response.xpath(
            '//div[@class="superangeloni-main-menu-0-x-mainMenuWrapper superangeloni-main-menu-0-x-mainMenuWrapperOpen "]/div/div/h4/a/@href'
        ).getall():
            yield scrapy.Request(
                url=self.domains + category,
                method="GET",
                callback=self.request_products,
            )

    def request_products(self, response):
        for products in response.xpath(
            '//div[@data-af-element="search-result"]/section/a/@href'
        ).getall():
            yield scrapy.Request(
                url=self.domains + products,
                method="GET",
                callback=self.product,
            )

    def product(self, response):

        price_integer = response.xpath(
            '//div[@style="height:auto"]/section/div/div/span[@class="superangeloni-store-theme-7-x-lowPrice"]/span/span[@class="superangeloni-store-theme-7-x-currencyInteger"]/text()'
        ).get()
        price_fraction = response.xpath(
            '//div[@style="height:auto"]/section/div/div/span[@class="superangeloni-store-theme-7-x-lowPrice"]/span/span[@class="superangeloni-store-theme-7-x-currencyFraction"]/text()'
        ).get()

        data_products = {
            "name": response.xpath(
                '//div[@style="height:auto"]/div/div/div/h1/span/text()'
            ).get(),
            "price": f"{price_integer}.{price_fraction}",
        }
        print(data_products)
