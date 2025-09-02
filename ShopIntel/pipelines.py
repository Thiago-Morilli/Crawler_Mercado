import os
import sys

from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ShopIntel.DataBase.models import Products, ProductsEans, Stores
from ShopIntel.DataBase.db import SQLAlchemyMethods

class SQLAlchemyPipeline:

    def __init__(self): 
        self.db = SQLAlchemyMethods()

    def insert_stores(self, data):
        existing = self.db.select_one(Stores, Stores.name == data["name"])
        if existing:
            return existing["id"]

        stores = Stores(
            name=data["name"],
         
        )
        item = self.db.insert_one(stores)
        return item["id"]

    def insert_product(self, item, stores_id):
        product = Products(
            name=item["name"],
            brand=item["brand"],
            sku=item["sku"],
            created_at=item.get("date", datetime.now()),
            price=item.get("price_from"),
            price_promotion=item["price"],
            id_store=stores_id
        )
        item = self.db.insert_one(product)
        return item["id"]

    def insert_ean(self, product_id, ean):
        ean_obj = ProductsEans(id_product=product_id, ean=ean)
        self.db.insert_one(ean_obj)


    def process_item(self, item, spider):
        stores_id = self.insert_stores(item.get("store"))
        product_id = self.insert_product(item, stores_id)

        self.insert_ean(product_id, item["ean"])

        return item