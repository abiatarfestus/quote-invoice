import random
from db import *
from faker import Faker
from datetime import datetime
from sqlalchemy import and_, or_, create_engine
from sqlalchemy.orm import sessionmaker

fake = Faker()

def get_connection():
    return create_engine(f"sqlite:///app_database.db")

# class DatabaseOps():
engine = get_connection()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# for i in range(5):
#     add_customer(
#         session, 
#         first_name=fake.first_name(), 
#         last_name=fake.last_name(), 
#         # entity_name=fake.first_name(), 
#         email=fake.ascii_free_email(), 
#         phone=fake.msisdn(), 
#         address=fake.address(), 
#         town=fake.city(), 
#         country=fake.country(),
#         customer_since=datetime.strptime(fake.date(), '%Y-%m-%d').date(),
#         notes=fake.sentence(nb_words=10)
#     )

#     add_customer(
#         session,
#         customer_type="Entity", 
#         entity_name=fake.company(), 
#         email=fake.company_email(), 
#         phone=fake.msisdn(), 
#         address=fake.address(), 
#         town=fake.city(), 
#         country=fake.country(),
#         customer_since=datetime.strptime(fake.date(), '%Y-%m-%d').date(),
#         notes=fake.sentence(nb_words=10)
#     )

# # # Add quotations-------------------------------------------
# customer_ids = [random.randint(1, 10) for i in range(5)]
# for i in range(5):
#     add_quotation(
#         session, 
#         quote_date=datetime.strptime(fake.date(), '%Y-%m-%d').date(),
#         description=fake.sentence(nb_words=3), 
#         customer_id=customer_ids[i], 
#         is_accepted=False,  
#         is_closed=False, 
#         notes=fake.sentence(nb_words=10)
#     )

# # Add orders-------------------------------------------
# customer_ids = [random.randint(1, 10) for i in range(5)]
# for i in range(5):
#     add_order(
#         session, 
#         order_date=datetime.strptime(fake.date(), '%Y-%m-%d').date(),
#         description=fake.sentence(nb_words=3), 
#         customer_id=customer_ids[i], 
#         is_paid=random.choice([False, True]), 
#         notes=fake.sentence(nb_words=10)
#     )

# # Add product-------------------------------------------
# for i in range(20):
#     add_product(
#         session, 
#         sku=f"SKU{fake.random_number(digits=5, fix_len=False)}",
#         barcode=fake.ean(length=13), 
#         product_name=fake.word(part_of_speech="noun"),
#         description=fake.sentence(nb_words=10),
#         price=float(fake.pricetag()[1:].replace(",", "")),
#         quantity=random.randint(1,200)
#     )

# # Add quotation item-------------------------------------------
# product_ids = [i for i in range(1,21)]
# for i in range(10):
#     add_quotation_item(
#         session, 
#         quote_id=random.randint(1,3),
#         product_id=i, 
#         quantity=random.randint(1,100), 
#         notes=fake.sentence(nb_words=10)
#     )

# # Add order item-------------------------------------------
# product_ids = [i for i in range(1,21)]
# for i in range(10):
#     add_order_item(
#         session, 
#         order_id=random.randint(1,3),
#         product_id=i, 
#         quantity=random.randint(1,100), 
#         notes=fake.sentence(nb_words=10)
#     )

# Delete quotations--------------------------------------
# quotations = get_quotations(session)
# for q in quotations:
#     session.delete(q)
# session.commit()

