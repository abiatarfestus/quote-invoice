import os
from moneyed import Money, NAD
from docxtpl import DocxTemplate
from datetime import datetime, timedelta
from quote_invoice.db import operations as db
from quote_invoice.db.models import Customer, QuotationItem, Product

class Quote():
    def __init__(self, session, quote_id, templates_dir="", output_dir=""):
        self.session = session
        self.quote_id = quote_id
        self.quote = db.get_quotations(self.session, pk=quote_id)
        # self.templates_dir = templates_dir
        # self.output_dir = output_dir
        self.doc = DocxTemplate("quote_template.docx")

    def generate_quote_preview(self):
        quote_id = self.quote.quote_id
        customer_id = self.quote.customer_id
        customer = db.get_customers(self.session, pk=customer_id)
        expiry_date = self.quote.quote_date + timedelta(days=30)
        expiry_date = str(expiry_date).replace("-", "/")
        quote_date = str(self.quote.quote_date).replace("-", "/")
        if customer.customer_type == "Person":
            customer_name = f"{customer.first_name} {customer.last_name}"
        else:
            customer_name = f"{customer.entity_name}"
        calculated_quote = self.calculate_quote(quote_id)
        context = {
            "quote_id": quote_id,
            "quote_date": quote_date,
            "expiry_date": expiry_date,
            "quote_description": self.quote.description,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "address": customer.address,
            "town": customer.town,
            "country": customer.country,
            "item_list": calculated_quote.get("item_list"),
            "subtotal": calculated_quote.get("subtotal"),
            "vat_rate":calculated_quote.get("vat_rate"),
            "vat_amount": calculated_quote.get("vat_amount"),
            "total_cost": calculated_quote.get("total_cost"),
        }
        self.doc.render(context)
        self.doc.save("generated_quote.docx")
        os.startfile("generated_quote.docx")
        return 

    def save_quote(self):
        pass

    def calculate_quote(self, quote_id):
        item_list = []
        subtotal = Money("0.00", NAD)
        vat_rate = 0.15
        quote_items = self.session.query(Product, QuotationItem).join(QuotationItem).filter(QuotationItem.quote_id == quote_id).all()
        for product,item in quote_items:
            unit_price = Money(product.price, NAD)
            total_price = unit_price*item.quantity
            item_list.append([
                product.product_name,
                item.description,
                item.quantity,
                unit_price.amount,
                total_price.amount,
            ])
            subtotal += total_price
        vat_amount = subtotal*vat_rate
        total_cost = vat_amount+subtotal
        vat_amount = str(vat_amount)
        subtotal = str(subtotal)
        total_cost = str(total_cost)
        calculated_quote = {
            "item_list": item_list,
            "subtotal": f"N${subtotal[3:]}",
            "vat_rate": f"{vat_rate:.0%}",
            "vat_amount": f"N${vat_amount[3:]}",
            "total_cost": f"N${total_cost[3:]}"
        }
        return calculated_quote
