import os
from moneyed import Money, NAD
from docxtpl import DocxTemplate
from datetime import timedelta
from tkinter import messagebox
from quote_invoice.db import operations as db
from quote_invoice.db.operations import get_settings
from quote_invoice.db.models import OrderItem, Product

class Invoice():
    def __init__(self, session, order_id, templates_dir="", output_dir=""):
        self.session = session
        self.order_id = order_id
        self.order = db.get_orders(self.session, pk=order_id)
        if self.order.is_paid:
            self.invoice_type = "TAX INVOICE"
        else:
            self.invoice_type = "PROFORMA INVOICE"
        self.settings =  get_settings(self.session)
        self.default_settings = False
        if self.settings and self.settings.invoice_template:
            self.vat_rate = float(self.settings.vat_rate)/100.0
            # self.invoice_validity = int(self.settings.invoice_validity)
            self.invoice_template = self.settings.invoice_template
            self.invoice_output_folder = self.settings.invoice_output_folder
            self.invoice_output_file = os.path.join(self.invoice_output_folder, "generated_invoice.docx")
        else:
            self.default_settings = True
            self.vat_rate = 0.15
            # self.invoice_validity = 30
            self.invoice_template = "invoice_template.docx"
            self.invoice_output_file = "generated_invoice.docx"
        self.doc = DocxTemplate(self.invoice_template)

    def generate_invoice_preview(self):
        if self.default_settings:
            if not messagebox.askyesno(
                message="Some settings have not been set. Default settings will be used instead. Do you want to proceed?",
                icon='question',
                title='Settings Warning'
            ):
                return
        order_id = self.order.order_id
        customer_id = self.order.customer_id
        customer = db.get_customers(self.session, pk=customer_id)
        # expiry_date = self.invoice.invoice_date + timedelta(days=self.invoice_validity)
        # expiry_date = str(expiry_date).replace("-", "/")
        # invoice_date = str(self.invoice.invoice_date).replace("-", "/")
        if customer.customer_type == "Person":
            customer_name = f"{customer.first_name} {customer.last_name}"
        else:
            customer_name = f"{customer.entity_name}"
        calculated_order = self.calculate_order(order_id)
        context = {
            "order_id": order_id,
            "order_date": self.order.order_date,
            # "expiry_date": expiry_date,
            "order_description": self.order.description,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "address": customer.address,
            "town": customer.town,
            "country": customer.country,
            "item_list": calculated_order.get("item_list"),
            "subtotal": calculated_order.get("subtotal"),
            "vat_rate":calculated_order.get("vat_rate"),
            "vat_amount": calculated_order.get("vat_amount"),
            "total_cost": calculated_order.get("total_cost"),
            "invoice_type": self.invoice_type
        }
        try:
            self.doc.render(context)
            self.doc.save(self.invoice_output_file)
            os.startfile(self.invoice_output_file)
            return
        except PermissionError as e:
            raise Exception(f"{e} Check if you have another open invoice and close it or save it with a different name. Then try again.")
        except Exception as e:
            raise Exception(f"Improperly configured settings. Check your folder settings: {e}")

    def calculate_order(self, order_id):
        item_list = []
        subtotal = Money("0.00", NAD)
        vat_rate = self.vat_rate
        order_items = self.session.query(Product, OrderItem).join(OrderItem).filter(OrderItem.order_id == order_id).all()
        for product,item in order_items:
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
        calculated_order = {
            "item_list": item_list,
            "subtotal": f"N${subtotal[3:]}",
            "vat_rate": self.settings.vat_rate, #f"{vat_rate:.2%}",
            "vat_amount": f"N${vat_amount[3:]}",
            "total_cost": f"N${total_cost[3:]}"
        }
        return calculated_order
