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
			'fieldtype':'Link',
			'options': 'Supplier',
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

def get_data(filters):
		pass