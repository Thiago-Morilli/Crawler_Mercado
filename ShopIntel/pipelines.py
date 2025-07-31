
from itemadapter import ItemAdapter
"""import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))"""
from ShopIntel.DataBase.db import SQLAlchemyMethods



class ShopintelPipeline(SQLAlchemyMethods):

    def process_item(self, item, spider):
        SQLAlchemyMethods().insert_one(item)
        return item

        # self.save_mysql(item, spider)

    # def save_mysql(self, item, spider):
    #     connector = Mysql_Connector.Connection()
    #     cursor = connector[0]
    #     db_connection = connector[1]

    #     self.name = spider.name

    #     cursor.execute(
    #        f'''CREATE TABLE IF NOT EXISTS {self.name}(
    #         name VARCHAR(200), 
    #         id INT,
    #         sku VARCHAR(50),
    #         price FLOAT,
    #         pricefrom FLOAT ,
    #         ean VARCHAR(100)
    #         )''' 
    #     ) 

    #     db_connection.commit()      

    #     insert_query = f"""
    #                     INSERT INTO  {self.name}(name, id, sku, price, pricefrom, ean)
    #                     VALUES (%s, %s, %s, %s, %s, %s)""" 
        
    #     cursor.execute(insert_query, [
    #             item.get("name"),
    #             item.get("id"),
    #             item.get("sku"),
    #             item.get("price"),
    #             item.get("pricefrom"),
    #             item.get("ean")

    #     ])
    #     db_connection.commit()
    #     print("Dados salvos com sucesso!")

    #     cursor.close()
    #     db_connection.close()