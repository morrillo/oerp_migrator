#!/usr/bin/python
# -*- coding: latin-1 -*-

import yaml
import xmlrpclib
import sys

import ConfigParser
import pdb
import logging


def get_field_type(oerp_origen,model):

	if not oerp_origen or not model:
		import pdb;pdb.set_trace()
		exit(1)
	args = [('model','=',model)]
	fields = ['name','ttype','relation','required']		
	model_search = 'ir.model.fields'
	args = [('model','=',model)]
        sock = oerp_origen['sock']
        field_ids = sock.execute(oerp_origen['dbname'],oerp_origen['uid'],oerp_origen['pwd'],model_search,'search',args)
        data = sock.execute(oerp_origen['dbname'],oerp_origen['uid'],oerp_origen['pwd'],model_search,'read',field_ids,fields)
	return_dict = {}
	for data_item in data:
		return_dict[data_item['name']] = [data_item['ttype'],data_item['relation'],data_item['required']]
	
	return return_dict

def get_lookup_ids(oerp_destino=None,relation_parm=None,ids_parm=None):
	
	if not oerp_destino or not relation_parm or not ids_parm:
		import pdb;pdb.set_trace()
		exit(1)
        sock = oerp_destino['sock']
	args = [('name','=',ids_parm[1])]
        obj_destino_ids = sock.execute(oerp_destino['dbname'],oerp_destino['uid'],oerp_destino['pwd'],relation_parm,'search',args)
	if obj_destino_ids:
		return obj_destino_ids[0]
	return 0
	

def read_models(config=None,section=None):
	if not config or not section:
		exit(1)
	return_dict = {}
	for dict_keys in config.keys():
		if dict_keys not in ['origin','destination']:
			fields = config[dict_keys]['fields']
			return_dict[dict_keys] = fields.split(',')
	return return_dict

def connect_openerp(dict_parms = None):
	if not dict_parms:
		exit(1)
		# Get the uid
	dict_connection = {}
	sock_common = xmlrpclib.ServerProxy ('http://'+dict_parms['hostname']+':'+str(dict_parms['port'])+'/xmlrpc/common')
	uid = sock_common.login(dict_parms['dbname'], dict_parms['username'], dict_parms['password'])

	#replace localhost with the address of the server
	sock = xmlrpclib.ServerProxy('http://'+dict_parms['hostname']+':'+str(dict_parms['port'])+'/xmlrpc/object')
	dict_connection['uid'] = uid
	dict_connection['pwd'] = dict_parms['password']
	dict_connection['dbname'] = dict_parms['dbname']
	dict_connection['sock'] = sock
	return dict_connection

def migrate_model(oerp_origen = None, oerp_destino = None, model = None, fields = None):
	if not oerp_origen or not oerp_destino or not model or not fields:
		exit(1)
	logging.getLogger(__name__).info("Migrando modelo %s"%(model))
	
	# data_obj = oerp_origen.get(model)
	sock = oerp_origen['sock']	
	data_ids = sock.execute(oerp_origen['dbname'],oerp_origen['uid'],oerp_origen['pwd'], model,'search',[])
	field_types = get_field_type(oerp_origen,model)
	data_items = sock.execute(oerp_origen['dbname'],oerp_origen['uid'],oerp_origen['pwd'], model,'read',data_ids,fields)

	for data in data_items:
		dict_insert = {}
		for field in fields:
			if field_types[field][0] not in ['many2many','one2many','many2one']:
				dict_insert[field] = data[field]
			else:
				if field_types[field][0] == 'many2one':
					if data[field]:
						dict_insert_field = get_lookup_ids(oerp_destino,field_types[field][1],data[field])
						if dict_insert_field <> 0:
							dict_insert[field] = dict_insert_field
						else:
							dict_insert[field] = data[field].id
					else:
						if field_types[field][2]:
							dict_insert[field] = 1
		#if model == 'res.partner':
		#	import pdb;pdb.set_trace()
		logging.getLogger(__name__).debug(dict_insert)
		sock_destino = oerp_destino['sock']
		data_items = sock_destino.execute(oerp_destino['dbname'],oerp_destino['uid'],oerp_destino['pwd'], model,'create',dict_insert)
	logging.getLogger(__name__).info("Fin migración modelo %s"%(model))
	return None

def main(configfile_parm = ''):

	logging.basicConfig(level=logging.DEBUG)
	logging.getLogger(__name__).info("Comenzando la migración")
	stream = file(configfile_parm,'r')
	dict_yaml = yaml.safe_load(stream)
	if not dict_yaml['origin'] or not dict_yaml['destination']:
		loggin.getLogger(__name__).error('No origin/destination specified in yaml file.')
		exit(1)
	dict_origin = dict_yaml['origin']	
	logging.getLogger(__name__).info("Origin host: %s port: %s database: %s"%(dict_origin['hostname'],dict_origin['port'],dict_origin['dbname']))
	dict_destination = dict_yaml['destination']
	logging.getLogger(__name__).info("Destination host: %s port: %s database: %s"%(dict_destination['hostname'],dict_destination['port'],dict_destination['dbname']))
	dict_models = read_models(dict_yaml,"objetos")
	oerp_origen = connect_openerp(dict_origin)
	oerp_destino = connect_openerp(dict_destination)

	for model,fields in dict_models.items():
		if model[0] != "#":
			migrate_model(oerp_origen,oerp_destino,model,fields)	
	logging.getLogger(__name__).info("Fin migración")
	exit(0)

if __name__ == "__main__":
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		print "Did not specify yaml file"
		exit(1)