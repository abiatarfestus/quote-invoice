from datetime import datetime
from sqlalchemy import and_, or_, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import asc, desc, func
from . models import Customer, Order, OrderItem, Quotation, QuotationItem, Product


# def get_connection():
#     return create_engine(f"sqlite:///app_database.db")

# # class DatabaseOps():
# engine = get_connection()
# Session = sessionmaker()
# Session.configure(bind=engine)
# session = Session()

def get_customers(session, pk=None, other_fields=""):
    """Get a list of customer objects sorted by last name"""
    if pk:
        return session.query(Customer).get(pk)
    elif other_fields == "":
        return session.query(Customer).order_by(Customer.customer_id).all()
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
            )
        .order_by(Customer.customer_id).all()
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
    country="Namibia",
    customer_since=None,
    notes=""
):
    try:
        session.query(Customer).filter(Customer.customer_id==pk).update({
            Customer.customer_type:customer_type, 
            Customer.first_name:first_name, 
            Customer.last_name:last_name, 
            Customer.entity_name:entity_name, 
            Customer.email:email, 
            Customer.phone:phone, 
            Customer.address:address, 
            Customer.town:town, 
            Customer.country:country,
            Customer.customer_since:customer_since,
            Customer.notes:notes
        }, synchronize_session=False
        )
        session.commit()
    except Exception as e:
        print(e)

def delete_customer(session, pk):
    try:
        customer = session.query(Customer).get(pk)
        session.delete(customer)
        session.commit()
    except Exception as e:
        print(e)

# Quotations -----------------------------------------------
def get_quotations(session, pk=None, customer_id=None, other_fields=""):
        if pk:
            return session.query(Quotation).get(pk)
        elif customer_id:
            return session.query(Quotation).filter(
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
                )
                .order_by(Quotation.quote_date).all()
            )
            return quotation
    
def add_quotation(
    session, 
    quote_date=datetime.today().date(),
    description="", 
    customer_id=None, 
    is_accepted=False, 
    is_closed=False,
    notes=""
):
    """Add a new quotation to the database and return its ID"""

    try:
        quotation = Quotation(
            quote_date=quote_date,
            description=description, 
            customer_id=customer_id, 
            is_accepted=is_accepted,  
            is_closed=is_closed,
            notes=notes
        )        
        session.add(quotation)
        session.commit()
        quote_id = quotation.quote_id
        # print(f"NEW QUOTE ID: {quote_id}")
        return quote_id
    except Exception as e:
        print(e)
        raise Exception(f"An error occurred while adding the quotation: {e}")

def update_quotation(
    session, 
    pk=None,
    # quote_date=datetime.today().date(),
    description="", 
    # customer_id=None, 
    is_accepted=False,
    # is_closed=False,
    notes=""
):
    try:
        session.query(Quotation).filter(Quotation.quote_id==pk).update({
            # Quotation.quote_date:quote_date,
            Quotation.description:description, 
            # Quotation.customer_id:customer_id, 
            Quotation.is_accepted:is_accepted, 
            # Quotation.is_closed:is_closed,
            Quotation.notes:notes
        }, synchronize_session=False
        )
        session.commit()
    except Exception as e:
        print(e)
    

def delete_quotation(session, pk):
    try:
        quotation = session.query(Quotation).get(pk)
        session.delete(quotation)
        session.commit()
    except Exception as e:
        print(e)
        raise Exception(f"An error occurred while adding the quotation: {e}")
    

# Orders -----------------------------------------------
def get_orders(session, pk=None, customer_id=None, other_fields=""):
        """Return order matching pk if pk is provided else orders matching customer_id or other_fiels"""
        if pk:
            return (session.query(Order).get(pk))
        elif customer_id:
            return session.query(Order).filter(
                Order.customer_id == customer_id
            ).order_by(Order.order_date).all()
        elif other_fields == "":
            return session.query(Order).order_by(Order.order_date).all()
        else:
            return (
                session.query(Order)
                .filter(
                    or_(
                        Order.description.like(f'%{other_fields}%'),
                        Order.notes.like(f'%{other_fields}%'),
                    )
                .order_by(Order.order_date).all()
                )
            )
    
def add_order(
    session, 
    order_date=datetime.today().date(),
    description="", 
    customer_id=None, 
    is_paid=False, 
    notes=""
):
    """Adds a new order to the database and return its ID"""

    try:
        order = Order(
            order_date=order_date,
            description=description, 
            customer_id=customer_id, 
            is_paid=is_paid, 
            notes=notes
        )
        session.add(order)
        session.commit()
        order_id = order.order_id
        # print(f"NEW ORDER ID: {order_id}")
        return order_id
    except Exception as e:
        print(e)
        raise Exception(f"An error occurred while adding the order: {e}")   
    

def update_order(
    session, 
    pk=None,
    # order_date=datetime.today(),
    description="", 
    # customer_id=None, 
    is_paid=False, 
    notes=""
):
    try:
        session.query(Order).filter(Order.order_id==pk).update({
            # Order.order_date:order_date,
            Order.description:description, 
            # Order.customer_id:customer_id, 
            Order.is_paid:is_paid, 
            Order.notes:notes
        }, synchronize_session=False
        )
        session.commit()
    except Exception as e:
        print(f"Update order: {e}")
        raise Exception(f"An error occurred while updating the order: {e}")

def delete_order(session, pk):
    try:
        order = session.query(Order).get(pk)
        session.delete(order)
        session.commit()
    except Exception as e:
        print(e)
        raise Exception(f"An error occurred while deleting the order: {e}")

    

# Quotation items -----------------------------------------------
def get_quotation_items(session, pk=None, quote_id=None):
        if pk:
            return session.query(QuotationItem).get(pk)
        else:
            return session.query(QuotationItem).filter(
                QuotationItem.quote_id == quote_id
            ).order_by(QuotationItem.quote_item_id).all()
            
def add_quotation_item(
    session, 
    quote_id=None,
    product_id=None, 
    quantity=1,
    description=""
):
    """Adds a new item to the quotation"""

    if quote_id and product_id:
        quotation = session.query(Quotation).get(quote_id)
        if quotation.is_closed:
            print("THIS QUOTATION IS CLOSED")
            return
        else:
            # Check if the product is already in the quotation
            # quotation_item = session.query(QuotationItem).filter(QuotationItem.product_id == product_id).one_or_none()
            if quotation.quotation_items: # If there are items in th quotation
                quote_items = quotation.quotation_items
                for item in quote_items:
                    if item.product_id == product_id:
                        # quotation_item.quantity += 1
                        print("THE SELECTED PRODUCT IS ALREADY ON THE QUOTATION")
                        return
            try:
                quotation_item = QuotationItem(
                    quote_id=quote_id,
                    product_id=product_id, 
                    quantity=quantity,
                    description=description
                )
                session.add(quotation_item)
                session.commit()
                return
            except Exception as e:
                print(e)
                raise Exception(f"An error occurred while adding a quote item: {e}")     
    

def update_quotation_item(
    session, 
    pk=None,
    # quote_id=None,
    # product_id=None, 
    quantity=0,
    description=""
):
    try:
        session.query(QuotationItem).filter(QuotationItem.quote_item_id==pk).update({
            # QuotationItem.quote_id:quote_id,
            # QuotationItem.product_id:product_id, 
            QuotationItem.quantity:quantity,
            QuotationItem.description:description
        }, synchronize_session = False
        )
        session.commit()
    except Exception as e:
        print(e)
        raise Exception(f"An error occurred while updating a quote item: {e}")
    

def delete_quotation_item(session, pk):
    try:
        quote_item = session.query(QuotationItem).get(pk)
        session.delete(quote_item)
        session.commit()
    except Exception as e:
        print(e)

# Order items -----------------------------------------------
def get_order_items(session, pk=None, order_id=None):
        if pk:
            return session.query(OrderItem).get(pk)
        else:
            return session.query(OrderItem).filter(
                OrderItem.order_id == order_id
            ).order_by(OrderItem.order_item_id).all()
            
def add_order_item(
    session, 
    order_id=None,
    product_id=None, 
    quantity=1,
    description=""
):
    """Add new item to the order"""

    if order_id and product_id:
        order = session.query(Order).get(order_id)
        # Check if the product is already in the order
        if order.order_items: # If there are items in th order
            order_items = order.order_items
            for item in order_items:
                if item.product_id == product_id:
                    raise Exception(f"Duplicate of product {item.product_id} found: Increase/decrease the quantity of the existing item instead.")
        try:
            order_item = OrderItem(
            order_id=order_id,
            product_id=product_id, 
            quantity=quantity,
            description=description
        )
            session.add(order_item)
            session.commit()
        except Exception as e:
            print(e)
            raise Exception(f"An error occurred while adding an order item: {e}")
    else:
        raise Exception ("Error: An item cannot be added without an order/product ID!")
    

def update_order_item(
    session, 
    pk=None,
    # order_id=None,
    # product_id=None, 
    quantity=0,
    description=""
):
    try:
        session.query(OrderItem).filter(OrderItem.order_item_id==pk).update({
            # OrderItem.order_id:order_id,
            # OrderItem.product_id:product_id, 
            OrderItem.quantity:quantity,
            OrderItem.description:description
        }, synchronize_session = False
        )
        session.commit()
    except Exception as e:
        print(f"Update order item: {e}")
        raise Exception(f"An error occurred while updating an order item: {e}")
    

def delete_order_item(session, pk):
    try:
        order_item = session.query(OrderItem).get(pk)
        session.delete(order_item)
        session.commit()
    except Exception as e:
        print(e)

# Products -----------------------------------------------
def get_products(session, pk=None, sku=None, barcode=None, product_name=""):
        if pk:
            return session.query(Product).get(pk)
        elif sku:
            return session.query(Product).filter(
                Product.sku.like(f'%{sku}%')
            ).order_by(Product.product_name).all()
        elif barcode:
            return session.query(Product).filter(
                Product.barcode.like(f'%{barcode}%')
            ).order_by(Product.product_name).all()
        elif product_name == "":
            return session.query(Product).order_by(Product.product_name).all()
        else:
            return session.query(Product).filter(
                Product.product_name.like(f'%{product_name}%')
            ).order_by(Product.product_name).all()
            
def add_product(
    session, 
    sku="",
    barcode="", 
    product_name="",
    description="",
    price=0.00,
    quantity=0
):
    """Adds a new product to the database"""

    # Check if product already exists
    product =  session.query(Product).filter(
        or_(Product.product_name == product_name,
        Product.barcode == barcode,
        Product.sku == sku
        )
    ).one_or_none()

    if product:
        print("PRODUCT ALREADY EXISTS")
        return
    else:
        try:
            product = Product(
                sku=sku,
                barcode=barcode, 
                product_name=product_name,
                description=description,
                price=price,
                quantity=quantity
            )
            session.add(product)
            session.commit()
        except Exception as e:
            print(e)      
    

def update_product(
    session, 
    pk=None,
    sku="",
    barcode="", 
    product_name="",
    description="",
    price=0.00,
    quantity=0
):
    try:
        session.query(Product).filter(Product.product_id==pk).update({
            Product.sku:sku,
            Product.barcode:barcode, 
            Product.product_name:product_name,
            Product.description:description,
            Product.price:price,
            Product.quantity:quantity,
        }, synchronize_session = False
        )
        session.commit()
    except Exception as e:
        print(e)
    

def delete_product(session, pk):
    try:
        product = session.query(Product).get(pk)
        session.delete(product)
        session.commit()
    except Exception as e:
        print(e)
    