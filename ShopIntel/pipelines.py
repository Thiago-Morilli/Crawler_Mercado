from ShopIntel.DataBase.db import Mysql_Connector 
from itemadapter import ItemAdapter


class ShopintelPipeline:

    def process_item(self, item, spider):

        self.save_mysql(item)

    def save_mysql(self, item):
        connector = Mysql_Connector.Connection()
        cursor = connector[0]
        db_connection = connector[1]

        cursor.execute(
           '''CREATE TABLE IF NOT EXISTS Markets(
            name VARCHAR(200), 
            id INT,
            sku VARCHAR(50),
            price INT,
            pricefrom INT,
            ean VARCHAR(200)
            )''' 
        )

        db_connection.commit()      

        insert_query = """
                        INSERT INTO  Markets(name, id, sku, price, pricefrom, ean)
                        VALUES (%s, %s, %s, %s, %s, %s)""" 
        
        cursor.execute(insert_query, [
                item["name"],
                item["id"],
                item["sku"],
                item["price"],
                item["pricefrom"],
                item["ean"]

        ])
        db_connection.commit()
        print("Dados salvos com sucesso!")

        cursor.close()
        db_connection.close()