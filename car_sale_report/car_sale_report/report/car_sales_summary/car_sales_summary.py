# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _
from frappe.utils import flt

def execute(filters=None):
	columns, data = [], []

	columns = get_columns(filters)
	data = get_data(filters)

	if not data:
		msgprint(_("No records found"))
		return columns, data
	
	return columns, data 

def get_columns(filters):
	return[
		{
			'fieldname':'serial_no',
			'label': _('Serial No'),
			'fieldtype':'Link',
			'options': 'Serial No',
			'width':'150',
		},
		{
			'fieldname':'supplier_name',
			'label': _('Supplier Name'),
			'fieldtype':'Data',
			# 'options': 'Supplier',
			'width':'250',
		},
		{
			'fieldname':'creation_document_no',
			'label': _('Creation Document No'),
			'fieldtype':'Purchase Invoice',
			'width':'120',
		},
		{
			'fieldname':'creation_date',
			'label': _('Creation Date'),
			'fieldtype':'Date',
			'width':'110',
		},
		{
			'fieldname':'incoming_rate',
			'label': _('Incoming Rate'),
			'fieldtype':'Currency',
			'width':'150',
		},
		{
			'fieldname':'delivery_document_no',
			'label': _('Delivery Document No'),
			'fieldtype':'Link',
			'options': 'Sales Invoice',
			'width':'150',
		},
		{
			'fieldname':'delivery_date',
			'label': _('Delivery Date'),
			'fieldtype':'Date',
			'width':'150'
		},
		{
			'fieldname':'customer_name',
			'label': _('Customer Name'),
			'fieldtype':'Data',
			'width':'150'
		},
		{
			'fieldname':'net_rate',
			'label': _('Net Rate'),
			'fieldtype':'Currency',
			'width':'150'
		},
		{
			'fieldname':'profit',
			'label': _('Profit'),
			'fieldtype':'Percent',
			'width':'150'
		},
	]


def get_rate_from_si_based_on_serial_no(serial_no,sales_invoice):
	print("serial_no,sales_invoice",serial_no,sales_invoice)
	inv_data = frappe.db.sql(
			"""select
				rate
			from
				`tabSales Invoice Item` tsii
			where
				CONCAT(tsii.serial_no, char(10)) like CONCAT("%%", %s, char(10), "%%")
				and parent = %s  limit 1 """,(serial_no,sales_invoice),
					as_dict=True,debug=1)	
	
	return inv_data		

def get_data(filters):
	data = frappe.db.sql(
			"""select
	name as serial_no,
	supplier ,
	supplier_name as supplier_name,
	purchase_document_no as creation_document_no,
	purchase_date as creation_date,
	purchase_rate as incoming_rate,
	sales_invoice as delivery_document_no,
	delivery_date as delivery_date,
	customer ,
	customer_name as customer_name,
	creation
from
	`tabSerial No`""", as_dict=True)	

	for row in data:
		if row.delivery_document_no != None:
			si_rate = get_rate_from_si_based_on_serial_no(row.serial_no, row.delivery_document_no)
			if len(si_rate) > 0 :
				row['net_rate'] = si_rate[0].rate
				if row.incoming_rate != 0 :
					row['profit'] = flt((((row.net_rate-row.incoming_rate) / row.incoming_rate) * 100), 2)
				else:
					row['net_rate'] = row.net_rate
					row['profit'] = 0					
		else:
			row['net_rate'] = 0
			row['profit'] = 0


	# print(data)

	return data	