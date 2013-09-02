from openerp.osv import osv,fields
import urllib as u
import string

class res_users(osv.osv):
	_name = "res.users"
	_inherit = "res.users"

	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
res_users()

class res_partner(osv.osv):
	_name = "res.partner"
	_inherit = "res.partner"
	
	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
	
res_partner()

class res_country_state(osv.osv):
	_name = "res.country.state"
	_inherit = "res.country.state"
	
	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
	
res_country_state()

class res_bank(osv.osv):
	_name = "res.bank"
	_inherit = "res.bank"
	
	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
	
res_bank()

class product_uom_categ(osv.osv):
	_name = "product.uom.categ"
	_inherit = "product.uom.categ"
	
	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
	
product_uom_categ()

class product_ul(osv.osv):
	_name = "product.ul"
	_inherit = "product.ul"
	
	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
	
product_ul()

class product_category(osv.osv):
	_name = "product.category"
	_inherit = "product.category"
	
	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
	
product_category()

class product_template(osv.osv):
	_name = "product.template"
	_inherit = "product.template"
	
	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
	
product_template()

class product_product(osv.osv):
	_name = "product.product"
	_inherit = "product.product"
	
	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
	
product_product()


class account_payment_term(osv.osv):
	_name = "account.payment.term"
	_inherit = "account.payment.term"
	
	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
	
account_payment_term()

class account_fiscalyear(osv.osv):
	_name = "account.fiscalyear"
	_inherit = "account.fiscalyear"
	
	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
	
account_fiscalyear()

class account_payment_term_line(osv.osv):
	_name = "account.payment.term.line"
	_inherit = "account.payment.term.line"
	
	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
	
account_payment_term_line()

class account_period(osv.osv):
	_name = "account.period"
	_inherit = "account.period"
	
	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
	
account_period()

class account_invoice(osv.osv):
	_name = "account.invoice"
	_inherit = "account.invoice"

	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
account_invoice()

class account_invoice_line(osv.osv):
	_name = "account.invoice.line"
	_inherit = "account.invoice.line"

	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
account_invoice_line()

class product_uom(osv.osv):
	_name = "product.uom"
	_inherit = "product.uom"

	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
product_uom()

class account_account(osv.osv):
	_name = "account.account"
	_inherit = "account.account"

	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
account_account()

class res_company(osv.osv):
	_name = "res.company"
	_inherit = "res.company"

	_columns = {
		'origin_id': fields.integer('Origin ID'),
		}
res_company()
