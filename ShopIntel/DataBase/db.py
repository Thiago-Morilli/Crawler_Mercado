from sqlalchemy import create_engine, text, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from ShopIntel.DataBase.test import Base


class SQLAlchemyDataPipeline:
    """
    SQLAlchemy Data Pipeline Class
    """
    user = os.getenv("mysqluser")
    password = os.getenv("mysqlpassword")
    host = os.getenv("mysqlhost")
    db_name = 'Products_Markets'
    print(user)

    def __init__(self):
        self.engine = self.connect_engine()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def connect_engine(self):
        engine_base = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}', echo=True)
        with engine_base.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.db_name}"))
            conn.execute(text(f"USE {self.db_name}"))
        # Agora conecta ao banco
        engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db_name}', echo=True)
        Base.metadata.create_all(engine)
        return engine

class SQLAlchemyMethods(SQLAlchemyDataPipeline):

    def insert_one(self, item):
        self.session.add(item)
        self.session.commit()
        print("k"*100)

        return {
            "id": item.id
        }
