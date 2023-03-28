from sqlalchemy import create_engine, Column, Float, Integer, String, ForeignKey, Date, Boolean
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
    customer_type = Column(String(6), nullable=False)
    first_name = Column(String(25))
    last_name = Column(String(25))
    entity_name = Column(String(50))
    email = Column(String(50), unique=True)
    phone = Column(String(10), nullable=False)
    address = Column(String(50))
    town = Column(String(25), nullable=False)
    country = Column(String(60))
    customer_since = Column(Date)
    notes = Column(String(250))
    quotations = relationship("Quotation", back_populates="customer")
    orders = relationship("Order", back_populates="customer")
    

class Quotation(Base):
    __tablename__ = "quotation"
    quote_id = Column(Integer, primary_key=True)
    quote_date = Column(Date)
    description = Column(String(250))
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    is_accepted = Column(Boolean)
    is_closed = Column(Boolean)
    notes = Column(String(250))
    customer = relationship("Customer", back_populates="quotations")
    quotation_items = relationship("QuotationItem", back_populates="quotation", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Quotation {self.quote_id}: {self.description}"
    

class QuotationItem(Base):
    __tablename__ = "quotation_item"
    quote_item_id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey("quotation.quote_id"))
    product_id = Column(Integer, ForeignKey("product.product_id"))
    quantity = Column(Integer)
    description = Column(String(100))
    quotation = relationship("Quotation", back_populates="quotation_items")

    # def __repr__(self):
    #     return f"Item {self.quote_item_id}: x{self.quantity} of Product: {self.product_id}"

class Order(Base):
    __tablename__ = "order"
    order_id = Column(Integer, primary_key=True)
    order_date = Column(Date)
    description = Column(String(100))
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    is_paid = Column(Boolean)
    notes = Column(String(250))
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Order {self.order_id}: {self.description}"
    

class OrderItem(Base):
    __tablename__ = "order_item"
    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.order_id"))
    product_id = Column(Integer, ForeignKey("product.product_id"))
    quantity = Column(Integer)
    description = Column(String(100))
    order = relationship("Order", back_populates="order_items")

    def __repr__(self):
        return f"Item {self.order_item_id}: x{self.quantity} of Product: {self.product_id}"

class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True)
    sku = Column(String(50), unique=True)
    barcode = Column(String(50), unique=True)
    product_name = Column(String(50), unique=True)
    description = Column(String(100))
    price = Column(String)
    quantity = Column(Integer)

class Settings(Base):
    __tablename__ = "settings"
    settings_id = Column(Integer, primary_key=True)
    quote_template = Column(String)
    invoice_template = Column(String)
    quote_output_folder = Column(String)
    invoice_output_folder = Column(String)
    vat_rate = Column(Float)
    quote_validity = Column(Integer)



# engine = get_connection()
# Base.metadata.create_all(engine)

