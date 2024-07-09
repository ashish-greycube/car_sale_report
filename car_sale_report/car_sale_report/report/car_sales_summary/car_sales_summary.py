# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _

def execute(filters=None):
	columns, data = [], []

	columns = get_columns(filters)
	data = get_data(filters)

	if not data:
		msgprint(_("No records found"))
		return columns, data
	
	return columns, data 

# Serial No (link)	Supplier Name (data)	Creation Document No (link PI)	
# Creation Date(date)	Incoming Rate(currency)	Delivery Document No(link SI)	
# Delivery Date(date)	Customer Name(data)	Net Rate(currency)	Profit(%)

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
	data = frappe.db.sql(
			"""select
				rate
			from
				`tabSales Invoice Item` tsii
			where
				concat(tsii.serial_no, char(10)) like concat('%', '%s', char(10), '%')
				and parent = '%s'  limit 1""",(serial_no,sales_invoice),
					as_dict=True,debug=1)	
	return data		

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
	customer_name as customer_name
from
	`tabSerial No`""")	

	return data	