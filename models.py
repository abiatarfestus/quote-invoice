from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Date, Boolean, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_connection():
    return create_engine(f"sqlite:///app_database.db")


# author_publisher = Table(
#     "author_publisher",
#     Base.metadata,
#     Column("author_id", Integer, ForeignKey("author.author_id")),
#     Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
# )

# book_publisher = Table(
#     "book_publisher",
#     Base.metadata,
#     Column("book_id", Integer, ForeignKey("book.book_id")),
#     Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
# )

class Customer(Base):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True)
    customer_type = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    entity_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    town = Column(String)
    country = Column(String)
    customer_since = Column(Date)
    notes = Column(String)
    quotations = relationship("Quotation", backref=backref("customer"))
    orders = relationship("Order", backref=backref("customer"))
    

class Quotation(Base):
    __tablename__ = "quotation"
    quote_id = Column(Integer, primary_key=True)
    quote_date = Column(Date)
    description = Column(String)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    is_accepted = Column(Boolean)
    is_closed = Column(Boolean)
    notes = Column(String)
    quotation_items = relationship("QuotationItem", backref=backref("quotation"))
    

class QuotationItem(Base):
    __tablename__ = "quotation_item"
    quote_item_id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey("quotation.quote_id"))
    product_id = Column(Integer, ForeignKey("product.product_id"))
    quantity = Column(Integer)
    notes = Column(String)

class Order(Base):
    __tablename__ = "order"
    order_id = Column(Integer, primary_key=True)
    order_date = Column(Date)
    description = Column(String)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    is_paid = Column(Boolean)
    notes = Column(String)
    order_items = relationship("OrderItem", backref=backref("order"))
    

class OrderItem(Base):
    __tablename__ = "order_item"
    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.order_id"))
    product_id = Column(Integer, ForeignKey("product.product_id"))
    quantity = Column(Integer)
    notes = Column(String)

class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True)
    sku = Column(String)
    barcode = Column(String)
    product_name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)



# engine = get_connection()
# Base.metadata.create_all(engine)

