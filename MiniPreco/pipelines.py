from itemadapter import ItemAdapter
from MiniPreco.Database.Mysql_connection import Mysql_Connector

class MiniprecoPipeline:
    def process_item(self, item, spider):

        self.save_mysql(item)

    def save_mysql(self, item):
        connector = Mysql_Connector.Connection()
        cursor = connector[0]
        db_connection = connector[1]

        cursor.execute(
           '''CREATE TABLE IF NOT EXISTS Products(
            name VARCHAR(100), 
            kilo_price VARCHAR(20),
            price VARCHAR(20),
            link VARCHAR(100) PRIMARY KEY
            );''' 
        )

        db_connection.commit()      

        insert_query = """
                        INSERT INTO  Products(name, kilo_price, price, link)
                        VALUES (%s, %s, %s, %s)""" 
        
        cursor.execute(insert_query, (
            item["name"],
            item["price"],
            item["kilo_price"],
            item["link"],
        ))

        db_connection.commit()
        print("Dados salvos com sucesso!")

        cursor.close()
        db_connection.close()