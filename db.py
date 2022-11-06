from models import *
from datetime import date
from sqlalchemy import and_, or_, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import asc, desc, func
from models import Customer, Order, OrderDetail, Quotation, QuotationDetail


# def get_connection():
#     return create_engine(f"sqlite:///app_db.db")

# # class DatabaseOps():
# engine = get_connection()
# Session = sessionmaker()
# Session.configure(bind=engine)
# session = Session()

def get_customers(session, pk=None, other_fields=""):
    """Get a list of customer objects sorted by last name"""
    if pk:
        customer = (
            session.query(Customer)
            .get(pk)
        )
    elif other_fields == "":
        return session.query(Customer).order_by(Customer.last_name).all()
    else:
        customer = (
            session.query(Customer)
            .filter(
                or_(
                    Customer.first_name.like(f'%{other_fields}%'),
                    Customer.last_name.like(f'%{other_fields}%'),
                    Customer.entity_name.like(f'%{other_fields}%'),
                    Customer.address.like(f'%{other_fields}%'),
                    Customer.phone.like(f'%{other_fields}%'),
                    Customer.email.like(f'%{other_fields}%'),
                    Customer.town.like(f'%{other_fields}%'),
                )
            .order_by(Customer.last_name).all()
            )
        )
    return customer
    
def add_customer(
    session, 
    customer_type="Person", 
    first_name="", 
    last_name="", 
    entity_name="", 
    email="", 
    phone="", 
    address="", 
    town="", 
    country="",
    customer_since=None,
    notes=""
):
    """Adds a new customer to the database"""

    # Check if the customer exists
    customer = (
        session.query(Customer)
        .filter(
            and_(
                Customer.first_name == first_name, Customer.last_name == last_name,
                or_(Customer.phone == phone, Customer.email == email)
            )
        )
        .one_or_none()
    )
    # Does the customer already exist?
    if customer is not None:
        return
    else:
        customer = Customer(
            customer_type=customer_type, 
            first_name=first_name, 
            last_name=last_name, 
            entity_name=entity_name, 
            email=email, 
            phone=phone, 
            address=address, 
            town=town, 
            country=country,
            customer_since=customer_since,
            notes=notes
        )
    
    session.add(customer)
    session.commit()

def update_customer(
    session, 
    pk=None,
    customer_type="Person", 
    first_name="", 
    last_name="", 
    entity_name="", 
    email="", 
    phone="", 
    address="", 
    town="", 
    country="",
    customer_since=None,
    notes=""
):
    try:
        session.query(Customer).get(pk).update(
            customer_type=customer_type, 
            first_name=first_name, 
            last_name=last_name, 
            entity_name=entity_name, 
            email=email, 
            phone=phone, 
            address=address, 
            town=town, 
            country=country,
            customer_since=customer_since,
            notes=notes
        )
    except Exception as e:
        print(e)
        return
    session.commit()

def delete_customer(session, pk):
    try:
        session.query(Customer).get(pk).delete()
    except Exception as e:
        print(e)
        return
    session.commit()

# Quotations -----------------------------------------------
def get_quotations(session, pk=None, customer_id=None, other_fields=""):
        if pk:
            quotation = (session.query(Quotation).get(pk))
        elif customer_id:
            return session.query(Customer).filter(
                Quotation.customer_id == customer_id
            ).order_by(Quotation.quote_date).all()
        elif other_fields == "":
            return session.query(Quotation).order_by(Quotation.quote_date).all()
        else:
            quotation = (
                session.query(Quotation)
                .filter(
                    or_(
                        Quotation.description.like(f'%{other_fields}%'),
                        Quotation.notes.like(f'%{other_fields}%'),
                    )
                .order_by(Quotation.quote_date).all()
                )
            )
        return quotation
    
def add_quotation(
    session, 
    quote_date=date.today(),
    description="", 
    customer_id=None, 
    is_accepted=False, 
    notes=""
):
    """Adds a new quotation to the database"""

    try:
        quotation = Quotation(
            quote_date=quote_date,
            description=description, 
            customer_id=customer_id, 
            is_accepted=is_accepted, 
            notes=notes
        )
    except Exception as e:
        print(e)
        return        
    session.add(quotation)
    session.commit()

def update_quotation(
    session, 
    pk=None,
    quote_date=date.today(),
    description="", 
    customer_id=None, 
    is_accepted=False, 
    notes=""
):
    try:
        session.query(Quotation).get(pk).update(
            cquote_date=quote_date,
            description=description, 
            customer_id=customer_id, 
            is_accepted=is_accepted, 
            notes=notes
        )
    except Exception as e:
        print(e)
        return
    session.commit()

def delete_quotation(session, pk):
    try:
        session.query(Quotation).get(pk).delete()
    except Exception as e:
        print(e)
        return
    session.commit()

# Orders -----------------------------------------------
def get_orders(session, pk=None, customer_id=None, other_fields=""):
        if pk:
            order = (session.query(Order).get(pk))
        elif customer_id:
            return session.query(Customer).filter(
                Order.customer_id == customer_id
            ).order_by(Order.order_date).all()
        elif other_fields == "":
            return session.query(Order).order_by(Order.order_date).all()
        else:
            order = (
                session.query(Order)
                .filter(
                    or_(
                        Order.description.like(f'%{other_fields}%'),
                        Order.notes.like(f'%{other_fields}%'),
                    )
                .order_by(Order.order_date).all()
                )
            )
        return order
    
def add_order(
    session, 
    order_date=date.today(),
    description="", 
    customer_id=None, 
    is_paid=False, 
    notes=""
):
    """Adds a new order to the database"""

    try:
        order = Order(
            order_date=order_date,
            description=description, 
            customer_id=customer_id, 
            is_paid=is_paid, 
            notes=notes
        )
    except Exception as e:
        print(e)
        return        
    session.add(order)
    session.commit()

def update_order(
    session, 
    pk=None,
    order_date=date.today(),
    description="", 
    customer_id=None, 
    is_paid=False, 
    notes=""
):
    try:
        session.query(Order).get(pk).update(
            corder_date=order_date,
            description=description, 
            customer_id=customer_id, 
            is_paid=is_paid, 
            notes=notes
        )
    except Exception as e:
        print(e)
        return
    session.commit()

def delete_order(session, pk):
    try:
        session.query(Order).get(pk).delete()
    except Exception as e:
        print(e)
        return
    session.commit()