# Copyright (c) 2023, Mubarrim and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MedicalStore(Document):
    def validate(self):
        self.make_ml_entry()

    def make_ml_entry(self):
        args = {"store_id": self.name, "doctype": "Medicine Ledger"}
        if frappe.db.exists(args):
            frappe.db.sql(
                """ delete from `tabMedicine Ledger` where store_id='%s' """ % self.name
            )

        args.update(
            {
                "store_name": self.store_name,
                "store_type": self.store_type,
                "store_city": self.store_city,
                "opening_hours": self.opening_hours,
                "street_address": self.street_address,
                "mobile_number": self.mobile_number,
                "contact_email": self.contact_email,
            }
        )

        for med in self.medicines:
            args.update(
                {
                    "medicine_formula": med.medicine_formula,
                    "medicine_name": med.medicine_name,
                    "medicine_type": med.medicine_type,
                    "medicine_price": med.medicine_price,
                }
            )
            if not frappe.db.exists(args):
                frappe.get_doc(args).insert(ignore_permissions=True)

    def on_trash(self):
        args = {"store_id": self.name, "doctype": "Medicine Ledger"}
        if frappe.db.exists(args):
            frappe.db.sql(
                """ delete from `tabMedicine Ledger` where store_id='%s' """ % self.name
            )

    def after_insert(self):
        if self.doctype == "Medical Store":
            # Create a user
            self.create_user_from_doc()
            self.create_user_permission_doc()

    def create_user_from_doc(self):
        # user_email = self.contact_email
        # user_name = self.contact_person

        # Create a new User
        frappe.get_doc(
            {
                "doctype": "User",
                "email": self.contact_email,
                "first_name": self.contact_person,
                "send_welcome_email": True,
                "role_profile_name": "Medical Store Profile",
                "module_profile": "Medical Store Module Profile",
            }
        ).insert(ignore_permissions=True)

    def create_user_permission_doc(self):
        # Create a new User Permission
        frappe.get_doc(
            {
                "doctype": "User Permission",
                "user": self.contact_email,
                "allow": "Medical Store",
                "for_value": self.name,
            }
        ).insert(ignore_permissions=True)
