import mysql.connector
import os


class Mysql_Connector:
    
    def Connection():
        db_connection = mysql.connector.connect(
            host=os.getenv("mysqlhost"),
            user=os.getenv("mysqluser"),
            password=os.getenv("mysqlpassword"),
            database="Markets"
        )

        if db_connection.is_connected():
            print("Conexão com o banco de dados está ativa.")
        else:
            print("Conexão com o banco de dados falhou.")

        cursor = db_connection.cursor()
        
        return [cursor, db_connection]