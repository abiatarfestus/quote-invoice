from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date, Boolean, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

author_publisher = Table(
    "author_publisher",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("author.author_id")),
    Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
)

book_publisher = Table(
    "book_publisher",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book.book_id")),
    Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
)

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
    orders = relationship("Quotation", backref=backref("customer"))
    # publishers = relationship(
    #     "Publisher", secondary=author_publisher, back_populates="authors"
    # )

class Quotation(Base):
    __tablename__ = "quotation"
    quote_id = Column(Integer, primary_key=True)
    quote_date = Column(Date)
    description = Column(String)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    is_accepted = Column(Boolean)
    notes = Column(String)
    order_details = relationship("QuotationDetail", backref=backref("quotation"))
    # publishers = relationship(
    #     "Publisher", secondary=book_publisher, back_populates="books"
    # )

class QuotationDetail(Base):
    __tablename__ = "quotation_detail"
    quote_detail_id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey("quotation.quote_id"))
    product_name = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    notes = Column(String)
    # publishers = relationship(
    #     "Publisher", secondary=book_publisher, back_populates="books"
    # )

class Order(Base):
    __tablename__ = "order"
    order_id = Column(Integer, primary_key=True)
    order_date = Column(Date)
    description = Column(String)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    is_paid = Column(Boolean)
    notes = Column(String)
    order_details = relationship("QuotationDetail", backref=backref("order"))
    # publishers = relationship(
    #     "Publisher", secondary=book_publisher, back_populates="books"
    # )

class OrderDetail(Base):
    __tablename__ = "order_detail"
    order_detail_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.order_id"))
    product_name = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    notes = Column(String)
    # publishers = relationship(
    #     "Publisher", secondary=book_publisher, back_populates="books"
    # )

