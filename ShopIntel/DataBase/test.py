from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, TIMESTAMP, BIGINT, DECIMAL, INTEGER, TEXT
from sqlalchemy.orm import relationship


Base = declarative_base()


class Products(Base):
    """
    Product Database Models
    """

    __tablename__ = "products"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(200), default=None)
    brand = Column(VARCHAR(200), default=None)
    sku = Column(VARCHAR(200), default=None)
    created_at = Column(TIMESTAMP, default=None)


    eans = relationship("ProductsEans", back_populates="product", cascade="all, delete-orphan")
    prices = relationship("Prices", back_populates="product", cascade="all, delete-orphan")


class ProductsEans(Base):
    """
    Product Eans Database Model
    """

    __tablename__ = "products_eans"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    id_product = Column(BIGINT)
    ean = Column(BIGINT, default=None)

    product = relationship("Products", back_populates="eans")



class Stores(Base):
    """
    Store Database Model
    """

    __tablename__ = "stores"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(200), default=None)

    prices = relationship("Prices", back_populates="store", cascade="all, delete-orphan")



class Prices(Base):
    """
    Price Database Model
    """

    __tablename__ = "prices"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    id_store = Column(INTEGER)
    id_product = Column(INTEGER)
    price = Column(DECIMAL(8, 2), default=None)
    price_promotion = Column(DECIMAL(8, 2), default=None)

    product = relationship("Products", back_populates="prices")
    store = relationship("Stores", back_populates="prices")
