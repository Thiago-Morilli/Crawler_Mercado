from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, TIMESTAMP, BIGINT, DECIMAL, INTEGER, TEXT


Base = declarative_base()


class Products(Base):
    """
    Product Database Models
    """

    __tablename__ = "products"

    id = Column(INTEGER, primary_key=True, autoincrement=True) 
    name = Column(VARCHAR(200), nullable=False)
    brand = Column(VARCHAR(200), default=None)
    sku = Column(VARCHAR(200), default=None)
    created_at = Column(TIMESTAMP)
    price = Column(DECIMAL(8, 2), default=None)
    price_promotion = Column(DECIMAL(8, 2), default=None)

    id_store = Column(INTEGER)

class ProductsEans(Base):
    """
    Product Eans Database Model 
    """

    __tablename__ = "products_eans"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    ean = Column(BIGINT, default=None)

    id_product = Column(INTEGER)

class Stores(Base):
    """
    Store Database Model
    """

    __tablename__ = "stores"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(200), nullable=False)

    id_product = Column(INTEGER)