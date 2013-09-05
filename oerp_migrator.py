#!/usr/bin/python
# -*- coding: latin-1 -*-

import yaml
import xmlrpclib
import sys

import ConfigParser
import pdb
import logging
from datetime import date

def get_date_from(oerp_destino=None):

	if not oerp_destino:
		import pdb;pdb.set_trace()
		exit(1)
	args = [('key','=','oerp_migrator_date_from')]
        sock = oerp_destino['sock']
        parameter_ids = sock.execute(oerp_destino['dbname'],oerp_destino['uid'],oerp_destino['pwd'],'ir.config_parameter','search',args)
	if not parameter_ids:
		return ''
        data = sock.execute(oerp_destino['dbname'],oerp_destino['uid'],oerp_destino['pwd'],'ir.config_parameter','read',parameter_ids,['value'])
	if data:
		return data['value']
	else:
		return ''

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
	else:
		#import pdb;pdb.set_trace()
		args = [('origin_id','=',ids_parm[0])]
		try:
	        	obj_destino_ids = sock.execute(oerp_destino['dbname'],oerp_destino['uid'],oerp_destino['pwd'],relation_parm,'search',args)
			if obj_destino_ids:
				return obj_destino_ids[0]
			else:
				return 0	
		except:
			logging.error("Problem looking up id for %s. Assigning default value"%(relation_parm))
			return 1
	return 0
	

def read_models(config=None,section=None):
	if not config or not section:
		exit(1)
	return_dict = {}
	for dict_keys in config.keys():
		return_dict[dict_keys] = {}
		if dict_keys not in ['origin','destination']:
			fields = config[dict_keys]['fields']
			return_dict[dict_keys]['sequence'] = config[dict_keys]['sequence']
			return_dict[dict_keys]['fields'] = fields.split(',')
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
	logging.info("Migrando modelo %s"%(model))
	
	# data_obj = oerp_origen.get(model)
	sock = oerp_origen['sock']	
	if get_date_from(oerp_destino) == '':
		data_ids = sock.execute(oerp_origen['dbname'],oerp_origen['uid'],oerp_origen['pwd'], model,'search',[])
	else:
		data_ids = sock.execute(oerp_origen['dbname'],oerp_origen['uid'],oerp_origen['pwd'], model,'search',[])
	field_types = get_field_type(oerp_origen,model)
	data_items = sock.execute(oerp_origen['dbname'],oerp_origen['uid'],oerp_origen['pwd'], model,'read',data_ids,fields)

	for data in data_items:
		dict_insert = {}
		for field in fields:
			if field in field_types:
				if field_types[field][0] not in ['many2many','one2many','many2one']:
					if field_types[field][0] != 'boolean' and data[field]:
						# if field_types[field][0] == 'char':
						dict_insert[field] = data[field]
					else:
						if data[field]:
							dict_insert[field] = data[field]
				else:
					if field_types[field][0] == 'many2one':
						if data[field]:
							dict_insert_field = get_lookup_ids(oerp_destino,field_types[field][1],data[field])
							if dict_insert_field <> 0:
								dict_insert[field] = dict_insert_field
							else:
								dict_insert[field] = data[field][0]
						else:
							if field_types[field][2]:
								dict_insert[field] = 1
		if 'id' not in dict_insert.keys():
			dict_insert['origin_id'] = data['id']
		logging.debug(dict_insert)
		sock_destino = oerp_destino['sock']
		destination_ids = sock_destino.execute(oerp_destino['dbname'],oerp_destino['uid'],oerp_destino['pwd'], \
			model,'search',[('origin_id','=',data['id'])])
		if destination_ids:
			data_items = sock_destino.execute(oerp_destino['dbname'],oerp_destino['uid'],oerp_destino['pwd'],\
				 model,'write',destination_ids,dict_insert)
		else:
			try:
				data_items = sock_destino.execute(oerp_destino['dbname'],oerp_destino['uid'],oerp_destino['pwd'],\
					 model,'create',dict_insert)
			except:
				import pdb;pdb.set_trace()
				pass
	logging.info("Fin migración modelo %s"%(model))
	return None

def validate_setup(dict_models = {}, oerp_destino = {}):
	if not dict_models:
		logging.error("No dict_models parameter in validate_setup")
		return False
	if not oerp_destino:
		logging.error("No oerp_destino parameter in validate_setup")
		return False

	for model in dict_models.keys():
		if model not in ['origin','destination']:
		        args = [('model','=',model)]
        		fields = ['name','ttype','relation','required']
	        	model_search = 'ir.model.fields'
	        	args = [('model','=',model),('name','=','origin_id')]
		        sock = oerp_destino['sock']
        		origin_ids = sock.execute(oerp_destino['dbname'],oerp_destino['uid'],oerp_destino['pwd'],model_search,'search',args)
			if not origin_ids:
				logging.error("Model "+model+" does not have origin_id column")
				return False
	
	return True


def main(configfile_parm = ''):

	logging.basicConfig(filename='/home/gustavo/work/biomed/migrator.log',level=logging.DEBUG)
	logging.info("Comenzando la migración")
	stream = file(configfile_parm,'r')
	dict_yaml = yaml.safe_load(stream)
	if not dict_yaml['origin'] or not dict_yaml['destination']:
		logging.error('No origin/destination specified in yaml file.')
		exit(1)
	dict_origin = dict_yaml['origin']	
	logging.info("Origin host: %s port: %s database: %s"%(dict_origin['hostname'],dict_origin['port'],dict_origin['dbname']))
	dict_destination = dict_yaml['destination']
	logging.info("Destination host: %s port: %s database: %s"%(dict_destination['hostname'],dict_destination['port'],dict_destination['dbname']))
	dict_models = read_models(dict_yaml,"objetos")
	for key,value in dict_models.items():
		logging.info(key)
		logging.info(value)
	oerp_origen = connect_openerp(dict_origin)
	oerp_destino = connect_openerp(dict_destination)
	if not validate_setup(dict_models,oerp_destino):
		logging.error("First you need to install the oerp_migrator_setup module in your OpenERP database.")
		exit(1)
	highest = 0
	for key in dict_models.keys():
		if 'sequence' in dict_models[key]:
			if dict_models[key]['sequence'] > highest:
				highest = dict_models[key]['sequence']

	for index in range(highest+1):
		for model,fields in dict_models.items():
			if model[0] !="#" and model not in ['origin','destination'] and fields['sequence'] == index:
				migrate_model(oerp_origen,oerp_destino,model,fields['fields'])	
	args = [('key','=','oerp_migrator_date_from')]
        sock = oerp_destino['sock']
        parameter_ids = sock.execute(oerp_destino['dbname'],oerp_destino['uid'],oerp_destino['pwd'],'ir.config_parameter','search',args)
	today = str(date.now())
	vals_parameter = { 'key': 'oerp_migrator_date_from',
			   'value': today }
	if not parameter_ids:
		ret_parameter_ids = soc.execute(oerp_destino['dbname',oerp_destino['uid'],oerp_destino['pwd'],\
			'ir.config_parameter','create',vals_parameter)	
	else:
		ret_parameter_ids = soc.execute(oerp_destino['dbname',oerp_destino['uid'],oerp_destino['pwd'],\
			'ir.config_parameter','write',parameter_ids,vals_parameter)	

	logging.info("Fin migración")
	exit(0)

if __name__ == "__main__":
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		print "Did not specify yaml file"
		exit(1)
