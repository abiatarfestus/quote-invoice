import os
from datetime import timedelta
from tkinter import messagebox

from docxtpl import DocxTemplate
from moneyed import NAD, Money

from quote_invoice.db import operations as db
from quote_invoice.db.models import Product, QuotationItem
from quote_invoice.db.operations import get_settings


class Quote:
    def __init__(self, session, quote_id):
        self.session = session
        self.quote_id = quote_id
        self.quote = db.get_quotations(self.session, pk=quote_id)
        self.settings = get_settings(self.session)
        self.default_settings = False
        if self.settings and self.settings.quote_template:
            self.vat_rate = float(self.settings.vat_rate)
            self.quote_validity = int(self.settings.quote_validity)
            self.quote_template = self.settings.quote_template
            self.quote_output_folder = self.settings.quote_output_folder
            self.quote_output_file = os.path.join(
                self.quote_output_folder, "generated_quote.docx"
            )
        else:
            self.default_settings = True
            self.vat_rate = 15.0
            self.quote_validity = 30
            self.quote_template = "quote_template.docx"
            self.quote_output_file = "generated_quote.docx"
        self.doc = DocxTemplate(self.quote_template)

    def generate_quote_preview(self):
        if self.default_settings:
            if not messagebox.askyesno(
                message="Some settings have not been set. Default settings will be used instead. Do you want to proceed?",
                icon="question",
                title="Settings Warning",
            ):
                return
        quote_id = self.quote.quote_id
        customer_id = self.quote.customer_id
        customer = db.get_customers(self.session, pk=customer_id)
        expiry_date = self.quote.quote_date + timedelta(days=self.quote_validity)
        # expiry_date = str(expiry_date).replace("-", "/")
        # quote_date = str(self.quote.quote_date).replace("-", "/")
        if customer.customer_type == "Person":
            customer_name = f"{customer.first_name} {customer.last_name}"
        else:
            customer_name = f"{customer.entity_name}"
        calculated_quote = self.calculate_quote(quote_id)
        context = {
            "quote_id": quote_id,
            "quote_date": self.quote.quote_date,
            "expiry_date": expiry_date,
            "quote_description": self.quote.description,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "address": customer.address,
            "town": customer.town,
            "country": customer.country,
            "item_list": calculated_quote.get("item_list"),
            "subtotal": calculated_quote.get("subtotal"),
            "vat_rate": calculated_quote.get("vat_rate"),
            "vat_amount": calculated_quote.get("vat_amount"),
            "total_cost": calculated_quote.get("total_cost"),
        }
        try:
            self.doc.render(context)
            self.doc.save(self.quote_output_file)
            os.startfile(self.quote_output_file)
            return
        except PermissionError as e:
            raise Exception(
                f"{e} Check if you have another open quote and close it or save it with a different name. Then try again."
            )
        except Exception as e:
            raise Exception(
                f"Improperly configured settings. Check your folder settings: {e}"
            )

    def calculate_quote(self, quote_id):
        item_list = []
        subtotal = Money("0.00", NAD)
        vat_rate = self.vat_rate
        quote_items = (
            self.session.query(Product, QuotationItem)
            .join(QuotationItem)
            .filter(QuotationItem.quote_id == quote_id)
            .all()
        )
        for product, item in quote_items:
            unit_price = Money(product.price, NAD)
            total_price = unit_price * item.quantity
            item_list.append(
                [
                    product.product_name,
                    item.description,
                    item.quantity,
                    unit_price.amount,
                    total_price.amount,
                ]
            )
            subtotal += total_price
        vat_amount = subtotal * (vat_rate/100)
        total_cost = vat_amount + subtotal
        # vat_amount = str(vat_amount)
        # subtotal = str(subtotal)
        # total_cost = str(total_cost)
        calculated_quote = {
            "item_list": item_list,
            # "subtotal": f"N${subtotal[3:]}",
            "subtotal": f"N${subtotal.amount}",
            "vat_rate": vat_rate,  # f"{vat_rate:.2%}",
            # "vat_amount": f"N${vat_amount[3:]}",
            "vat_amount": f"N${vat_amount.amount:.2f}",
            # "total_cost": f"N${total_cost[3:]}",
            "total_cost": f"N${total_cost.amount:.2f}",
        }
        return calculated_quote
