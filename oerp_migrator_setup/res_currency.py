from osv import osv,fields
import urllib as u
import string

class res_currency_rate(osv.osv):
	_name = "res.currency.rate"
	_inherit = "res.currency.rate"
	
	def currency_schedule_update(self,cr,uid,context=None):

		data = []
		url = 'http://download.finance.yahoo.com/d/quotes.csv?s=USDARS=X&f=sl1d1t1ba&e=.csv'
		f = u.urlopen(url,proxies = {})
		rows = f.readlines()
		for r in rows:
			values = [x for x in r.split(',')]
			bid = string.atof(values[1])

	        currency_obj = self.pool.get('res.currency')
	        currency_rate_obj = self.pool.get('res.currency.rate')
                currency_id = currency_obj.search(cr, uid, [('name', '=', 'USD')])
		print "Actualizacion %s" % bid
		if not currency_id:
			print "No esta cargado el peso argentino"
		else:
			values = {
				'rate': values[1],
				'currency_id': currency_id[0],
				'currency_type_id': ''
				}
			currency_rate_obj.create(cr,uid,values)

		return True
	
res_currency_rate()
