from osv import osv,fields
import urllib as u
import string

class res_partner(osv.osv):
	_name = "res.partner"
	_inherit = "res.partner"
	
	columns = {
		'origin_id': fields.integer('Origin ID')
		}
	
res_partner()

class res_country_state(osv.osv):
	_name = "res.country.state"
	_inherit = "res.country.state"
	
	columns = {
		'origin_id': fields.integer('Origin ID')
		}
	
res_country_state()

class res_bank(osv.osv):
	_name = "res.bank"
	_inherit = "res.bank"
	
	columns = {
		'origin_id': fields.integer('Origin ID')
		}
	
res_bank()
