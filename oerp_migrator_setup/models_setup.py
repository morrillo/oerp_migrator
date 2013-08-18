from openerp.osv import osv,fields
import urllib as u
import string

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
