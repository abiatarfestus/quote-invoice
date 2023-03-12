from datetime import datetime
from sqlalchemy import and_, or_, create_engine
from sqlalchemy.orm import sessionmaker
from . models import Customer, Order, OrderItem, Quotation, QuotationItem, Product

def get_connection():
    return create_engine(f"sqlite:///app_database.db")

# class DatabaseOps():
engine = get_connection()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


# show quotations with items---------------------------------
# quotations = session.query(Quotation).all()

# for quote in quotations:
#     print("")
#     print(f"Quote: {quote.quote_id}: {quote.description}")
#     for quote_item in quote.quotation_items:
#         product = session.query(Product).get(quote_item.product_id)
#         print(f"{product.product_name}\t\t x{quote_item.quantity}\t@ N${product.price * quote_item.quantity}")
#     print("")

# # show orders with items---------------------------------
# orders = session.query(Order).all()

# for order in orders:
#     print("")
#     print(f"Order: {order.order_id}: {order.description}")
#     for order_item in order.order_items:
#         product = session.query(Product).get(order_item.product_id)
#         print(f"{product.product_name}\t\t x{order_item.quantity}\t@ N${product.price * order_item.quantity}")
#     print("")

# # show customers with their quotations---------------------------------
# customers = session.query(Customer).all()

# for customer in customers:
#     if len(customer.quotations) > 0:
#         print("")
#         if customer.first_name:
#             print(f"Customer: {customer.first_name} {customer.last_name}")
#         else:
#             print(f"Customer: {customer.entity_name}")
#         for quote in customer.quotations:
#             print(quote)

# show customers with their orders---------------------------------
customers = session.query(Customer).all()

for customer in customers:
    if len(customer.orders) > 0:
        print("")
        if customer.first_name:
            print(f"Customer: {customer.first_name} {customer.last_name}")
        else:
            print(f"Customer: {customer.entity_name}")
        for order in customer.orders:
            print(order)

