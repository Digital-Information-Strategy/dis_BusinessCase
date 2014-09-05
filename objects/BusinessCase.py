# -*- coding: utf-8 -*-
##############################################################################
#
#	OpenERP, Open Source Management Solution
#	Copyright (C) 2013 DIS S.A. (<http://www.dis.co.cr>).
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from datetime import datetime
import openerp.addons.decimal_precision as dp
from bzrlib.transport import readonly
import base64
import binascii
import csv
import time


class business_case(osv.osv):

	_name = 'business.case'
	_inherit = ['mail.thread'] # SUBIR A RAMA
	def default_horas_totales(self, cr, uid, ids, context=None):
		model_data=self.pool.get('bc.areas.especialidad')
		conditions = model_data.search(cr, uid, [])
		e = model_data.read(cr, uid, conditions)
		result=[]
		for a in e:
			result.append({'area_id':a['id']})
		return result
	
	def default_aprobaciones_id(self, cr, uid, ids, context=None):
		model_data=self.pool.get('bc.aprobaciones.departamento')
		conditions = model_data.search(cr, uid, [])
		e = model_data.read(cr, uid, conditions)
		result=[]
		for a in e:
			result.append({'name':a['id']})
		return result
	
	def default_viaticos_totales(self, cr, uid, ids, context=None):
		model_data=self.pool.get('bc.areas.especialidad')
		conditions = model_data.search(cr, uid, [])
		e = model_data.read(cr, uid, conditions)
		result=[]
		for a in e:
			result.append({'sub_categoria_id':a['id']})
		return result
	
	def default_adicionales_totales(self, cr, uid, ids, context=None):
		model_data=self.pool.get('bc.areas.especialidad')
		conditions = model_data.search(cr, uid, [])
		e = model_data.read(cr, uid, conditions)
		result=[]
		for a in e:
			result.append({'area_id':a['id']})
		return result
	
	def default_ingreso_propuesto(self, cr, uid, ids, context=None):
		model_data=self.pool.get('bc.cdo')
		conditions = model_data.search(cr, uid, [])
		e = model_data.read(cr, uid, conditions)
		result=[]
		for a in e:
			result.append({'cdo_id':a['id']})
		return result
	
	def default_margen_operacion(self, cr, uid, ids, context=None):
		model_data=self.pool.get('bc.cdo.margen')
		conditions = model_data.search(cr, uid, [])
		e = model_data.read(cr, uid, conditions)
		result=[]
		for a in e:
			result.append({'name':a['id']})
		return result
	
	def default_indicadores(self, cr, uid, ids, context=None):
		model_data=self.pool.get('bc.indicadores')
		conditions = model_data.search(cr, uid, [])
		e = model_data.read(cr, uid, conditions)
		result=[]
		for a in e:
			result.append({'name':a['id']})
		return result

	def default_ingreso_propuesto_superior(self, cr, uid, ids, context=None):
		model_data=self.pool.get('bc.areas.especialidad')
		conditions = model_data.search(cr, uid, [])
		e = model_data.read(cr, uid, conditions)
		result=[]
		for a in e:
			result.append({'area_id':a['id']})
		return result
	def default_costo_operacion(self, cr, uid, ids, context=None):
		model_data=self.pool.get('bc.areas.especialidad')
		conditions = model_data.search(cr, uid, [])
		e = model_data.read(cr, uid, conditions)
		result=[]
		for a in e:
			result.append({'area_id':a['id']})
		return result
	def default_margen_contribucion(self, cr, uid, ids, context=None):
		model_data=self.pool.get('bc.areas.especialidad')
		conditions = model_data.search(cr, uid, [])
		e = model_data.read(cr, uid, conditions)
		result=[]
		for a in e:
			result.append({'area_id':a['id'],'porc_contribucion':100})
		return result
	
	def _get_client(self, cr, uid, ids, name, args, context=None):
		result={}
		cliente=[0]
		id1=0
		valor=0
		for i in self.browse(cr,uid,ids,context=context):
			id1=i.id
			valor=i.oportunidad_id.id
		if valor!=False:
			model_data=self.pool.get('crm.lead')
			conditions = model_data.search(cr, uid, [('id', '=', valor)])
			i = model_data.read(cr, uid, conditions)
			cliente=i[0]['partner_id']
			result[id1]=cliente
		else:
			result[id1]=0
		#print "result "+str(result)
		return result
	
	def _get_pedido_venta_v(self, cr, uid, ids, name, args, context=None):
		state = ""
		vec={}
		for i in self.browse(cr,uid,ids,context=context):
			#id1=i.id
			state=i.pedido_venta.state
			vec[i.id]=state
		#print "---- state ----" + str(state)
		#print "HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAA "+str(vec) asd
		if vec[i.id]==None:
			vec[i.id]='draft'
			return vec
		else:
			print "acaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa: "+str(vec)
			return vec

	_columns = {
	# ----------------  Para encabezado  ----------------
	'name': fields.char('Referencia',size=128, readonly=True, states={'draft':[('readonly',False)]}),
	'state': fields.selection([('draft','Borrador'),('sale','Venta'),('done','Realizado'),('cancel','Cancelado')], 'Estado'),
	'date': fields.date('Fecha de creación',readonly=True, states={'draft':[('readonly',False)]}),
	'number': fields.char('Número', size=64, readonly=True),
	'version': fields.integer('Version', readonly=True),
	# ---------------- Para pestaña de Generalidades en BC. --------------------
	'bc_padre_id': fields.many2one('business.case','Business Case Padre'),
	'oportunidad_id': fields.many2one('crm.lead','Oportunidad', required=True, domain="[('type','=','opportunity')]", readonly=True, states={'draft':[('readonly',False)]}, create=['dis_BusinessCase.group_bc_manager','dis_BusinessCase.group_bc_sale']),
	'user_id': fields.many2one('res.users',' Consultor',readonly=True, states={'draft':[('readonly',False)]}),
	#'cliente_id': fields.many2one('res.partner','Razón social del cliente', readonly=True),
	'cliente_id': fields.function(_get_client, string='Razón social del cliente',type='many2one', relation='res.partner', store=True),
	#'cliente_nombre': fields.many2one('res.partner','Razón social del cliente', size=128, readonly=True), 
	'proyecto_id': fields.many2one('project.project','Nombre del Proyecto', readonly=True), # POR EL MOMENTO ESTE ESTARÁ COMO TIPO CHAR X FALTA DE MÓDULO PROYECTOS
	'contactos_id': fields.one2many('res.partner', 'parent_id_bc', 'Contactos', domain=[('active','=',True)]), #fields.char('Contacto del cliente', size=128),	
	'telefono_cliente': fields.char('Teléfono del cliente', size=128, readonly=False), # Definir luego size del teléfono
	'direccion_entrega': fields.char('Dirección de entrega', size=128,readonly=False), 
	'email_cliente': fields.char('E-mail del cliente', size=128, readonly=False), 
	'orden_compra': fields.many2one('purchase.order','Orden de Compra', readonly=True), # ASOCIAR A ORDENES DE COMPRA
	'orden_compra_externa': fields.char('Orden de Compra Externa', readonly=True), 
	'pedido_venta': fields.many2one('sale.order','Pedido de Venta', readonly=True),
	'deal_fabricantes': fields.char('Deal Ids de los fabricantes', size=128, states={'done':[('readonly',True)]}),  #De dónde viene?
	'fecha_entrega_equipos': fields.date('Fecha de entrega de equipos', states={'done':[('readonly',True)]}), #De dónde viene?
	'fecha_entrega_servicios': fields.date('Fecha de entrega de servicios', states={'done':[('readonly',True)]}), #De dónde viene?
	
	
	
	
	
	'garantia': fields.char('Garantía', size=128, states={'done':[('readonly',True)]}),
	'vigencia_oferta': fields.char('Vigencia de la Oferta', size=128, states={'done':[('readonly',True)]}),
	'condiciones_pago': fields.char('Condiciones de Pago', size=128, states={'done':[('readonly',True)]}),
			
					
							
									
											
															
	'bc_observaciones': fields.text('Observaciones',readonly=True, states={'draft':[('readonly',False)]}),
	#'aprobaciones_id':
	'aprobaciones_id': fields.one2many('bc.aprobaciones','bc_id','Aprobaciones',readonly=True, states={'draft':[('readonly',False)]}),

	# ---------------- Para pestaña de Descripción del servicio. --------------------
	'solucion': fields.char('Nombre de solución ofertada', size=128,readonly=True, states={'draft':[('readonly',False)]}),
	'cliente_requerimientos': fields.text('Requerimientos del cliente',readonly=True, states={'draft':[('readonly',False)]}),
	'descripcion_solucion': fields.text('Descripción de la solución (alcances)',readonly=True, states={'draft':[('readonly',False)]}),
	'factores_criticos': fields.text('Factores críticos de éxito',readonly=True, states={'draft':[('readonly',False)]}),
	'elementos_fuera': fields.text('Elementos fuera de alcance',readonly=True, states={'draft':[('readonly',False)]}),
 
	# ---------------- Para pestaña Costos Operativos. --------------------
	# Horas de trabajo
	'horas_id': fields.one2many('bc.horas','bc_id','Horas de trabajo',readonly=True, states={'draft':[('readonly',False)]}),
	'horas_totales_id': fields.one2many('bc.totales.horas','bc_id','Total horas de trabajo',readonly=True),
	# Viáticos
	'viaticos_id': fields.one2many('bc.viaticos','bc_id','Viáticos',readonly=True, states={'draft':[('readonly',False)]}),
	'totales_viaticos_id': fields.one2many('bc.totales.viaticos','bc_id','Total viáticos', readonly=True),
	# Materiales Adicionales
	'adicionales_id': fields.one2many('bc.materiles.adicionales','bc_id','Materiales Adicionales',readonly=True, states={'draft':[('readonly',False)]}),
	'totales_adicionales_id': fields.one2many('bc.totales.adicionales','bc_id','Totales', readonly=True),
	# Ingreso propuesto
	'ingreso_propuesto_id':fields.one2many('bc.ingreso.presupuestado','bc_id','Ingreso Propuesto2',readonly=True, states={'draft':[('readonly',False)]}),
	'ingreso_propuesto_superior_id':fields.one2many('bc.ingreso.propuesto','bc_id','Ingreso Propuesto', states={'done':[('readonly',True)]}),
	'costo_operacion_id':fields.one2many('bc.costo.operacion','bc_id','Costo Operacion',readonly=True, states={'draft':[('readonly',False)]}),
	'margen_contribucion_id':fields.one2many('bc.margen.contribucion','bc_id','Margen Contribucion', states={'done':[('readonly',True)]}),

	'implementacion_costo': fields.float('$',readonly=True),
	'implementacion_costo_por': fields.float('%',readonly=True),
	
	'mantenimientos_costo': fields.float('$',readonly=True),
	'mantenimientos_costo_por': fields.float('%',readonly=True),
	
	'infra_costo': fields.float('$',readonly=True),
	'infra_costo_por': fields.float('%',readonly=True),
	
	'noc_costo': fields.float('$',readonly=True),
	'noc_costo_por': fields.float('%',readonly=True),
	
	'implementacion_margen': fields.float('$',readonly=True),
	'implementacion_margen_por': fields.float('%', readonly=True, states={'draft':[('readonly',False)]}),
	
	'mantenimientos_margen': fields.float('$',readonly=True),
	'mantenimientos_margen_por': fields.float('%',readonly=True, states={'draft':[('readonly',False)]}),
	
	'infra_margen': fields.float('$',readonly=True),
	'infra_margen_por': fields.float('%',readonly=True, states={'draft':[('readonly',False)]}),
	
	'noc_margen': fields.float('$',readonly=True),
	'noc_margen_por': fields.float('%',readonly=True, states={'draft':[('readonly',False)]}),
	#Seccion de arriba de la tabla.
	'implementacion_ip': fields.float('$',readonly=True),
	'implementacion_ip_por': fields.float('%',readonly=True, states={'draft':[('readonly',False)],'sale':[('readonly',False)]}),
	'mantenimientos_ip': fields.float('$',readonly=True),
	'mantenimientos_ip_por': fields.float('%',readonly=True, states={'draft':[('readonly',False)],'sale':[('readonly',False)]}),
	'infra_ip': fields.float('$',readonly=True),
	'infra_ip_por': fields.float('%',readonly=True, states={'draft':[('readonly',False)],'sale':[('readonly',False)]}),
	'noc_ip': fields.float('$',readonly=True),
	'noc_ip_por': fields.float('%',readonly=True, states={'draft':[('readonly',False)],'sale':[('readonly',False)]}),
	# Notas Adicionales
	'bc_notas_adicionales': fields.text('Observaciones'),

	# ---------------- Para pestaña BOM Equipo. --------------------
	'bom_equipo_id': fields.one2many('bc.bom.equipo','bc_id','BOM Equipo'),

	# ---------------- Para pestaña Margen de Operación. --------------------
	'bc_margen_operacion_id': fields.one2many('bc.margen.operacion','bc_id','Ingreso Propuesto'),
	# Ingreso propuesto
	'ingreso_implementacion': fields.float('Ingreso', readonly=True),
	'porc_ingreso_implementacion': fields.float('% Ingreso', readonly=True),
	'ingreso_mantenimientos': fields.float('Ingreso', readonly=True),
	'porc_ingreso_mantenimientos': fields.float('% Ingreso', readonly=True),
	'ingreso_noc': fields.float('Ingreso', readonly=True),
	'porc_ingreso_noc': fields.float('% Ingreso', readonly=True),
	'ingreso_infraestructura': fields.float('Ingreso', readonly=True),
	'porc_ingreso_infraestructura': fields.float('% Ingreso', readonly=True),
	'ingreso_equipos': fields.float('Ingreso', readonly=True),
	'porc_ingreso_equipos': fields.float('% Ingreso', readonly=True),
	'ingreso_total': fields.float('Ingreso', readonly=True),
	'porc_ingreso_total': fields.float('% Ingreso', readonly=True),
	# Indicadores
	'bc_montos_indicadores_id': fields.one2many('bc.montos.indicadores','bc_id','Indicadores'),
	# Costos de operación
	'costo_implementacion': fields.float('Ingreso'), 
	'porc_costo_implementacion': fields.float('% Ingreso'),
	'costo_mantenimientos': fields.float('Ingreso'),
	'porc_costo_mantenimientos': fields.float('% Ingreso'),
	'costo_noc': fields.float('Ingreso'),
	'porc_costo_noc': fields.float('% Ingreso'),
	'costo_infraestructura': fields.float('Ingreso'),
	'porc_costo_infraestructura': fields.float('% Ingreso'),
	'costo_equipos': fields.float('Ingreso'),
	'porc_costo_equipos': fields.float('% Ingreso'),
	'costo_total': fields.float('Ingreso'),
	'porc_costo_total': fields.float('% Ingreso'),
	# Número de FTE
	'fte_implementacion': fields.float('Monto'), 
	'fte_mantenimientos': fields.float('Monto'),
	'fte_noc': fields.float('Monto'),
	'fte_infraestructura': fields.float('Monto'),
	'fte_equipos': fields.float('Monto'),
	'fte_total': fields.float('Monto'),
	'archivo': fields.binary('archivo'),
	# Cuadro resumen en Margen Operación
	'resumen_ingreso': fields.float('Ingreso Presupuestado'),
	'resumen_egreso': fields.float('Egresos Presupuestados'),
	'resumen_utilidad': fields.float('Utilidad'),
	# Cuadro resumen en Generalidades
	'resumen_ingreso_c': fields.float('Ingreso Presupuestado'),
	'resumen_egreso_c': fields.float('Egresos Presupuestados'),
	'resumen_utilidad_c': fields.float('Utilidad'),
	# Para boton cancelar.
	'pedido_venta_validado': fields.function(_get_pedido_venta_v, string='Pedido venta validado',type='char', store=False),
	}
	_defaults = {
	'pedido_venta_validado':'draft',
	'version': 1,
	'date': datetime.now().strftime('%Y-%m-%d'),
	'state': 'draft',
	'horas_totales_id': default_horas_totales,
	'aprobaciones_id': default_aprobaciones_id,
	'totales_viaticos_id': default_viaticos_totales,
	'totales_adicionales_id': default_adicionales_totales,
	'ingreso_propuesto_id': default_ingreso_propuesto,
	'bc_margen_operacion_id': default_margen_operacion,
	'bc_montos_indicadores_id': default_indicadores,
	'ingreso_propuesto_superior_id': default_ingreso_propuesto_superior,
	'costo_operacion_id': default_costo_operacion,
	'margen_contribucion_id': default_margen_contribucion,

 	}
	
	def product_id_change(self, cr, uid, ids,product, context=None):
		res =res = self.pool.get('product.product').browse(cr, uid, product, context=context)
		if product!=False: return {'value':{'codigo_producto' :res.code,'descripcion_producto' :res.name}}
		else: return {'value':{'codigo_producto' :'','descripcion_producto' :''}}

	def get_codigo(self, cr, uid, ids,letras, context=None):
		res = self.pool.get('product.product').name_search(cr, uid, letras, args=None, operator='ilike', context=None, limit=100)
		#print '\n\n'+str(res)+'\n\n'
		return res#{'value':{'descripcion_producto' :'aaaa'}}
	
	def onchange_archivo(self, cr, uid, ids,archivo, context=None):
		#archivo = context['archivo']
		archivo=archivo
		#print '\n\narchivo '+str(archivo)+'\n\n'
		if archivo==False:
			d=self.write(cr, uid, ids, {'archivo': False,},context=context)
			return {'value': {'archivo': False}}

			#return {'value': {'archivo': False,}}
		reader = csv.reader(str(base64.b64decode(archivo)).replace('\r','\n').split('\n'),delimiter='\r')#SIRVE
		#reader = csv.reader(str(binascii.a2b_base64(archivo)).replace('\r\n','\n').split('\n'),delimiter='\r')
		#print 'reader= '+str(reader)
		#ofile  = open('Dropbox/Dropbox/addons/mi_modulo/archivito.csv', "wb")
		#writer = csv.writer(ofile, quoting=csv.QUOTE_NONE)
		rellena=[]
		rellena1=[]
		cont=0
		contt=0
		for row in reader:
			print 'row '+str(row)
			if contt>0:
				if len(row)>0:
				
					r=row[0].split(';')
					print "............. rrrr .........." + str(r)
					val=self.get_codigo(cr, uid, ids,r[0], context=context)
					val2=[]
					vall2=0
					if r[4]!='':					
						query="select id from res_partner where name='"+str(r[4])+"'"
						cr.execute(query)
						valor_res=cr.dictfetchall()[0].get('id')
						vall2=valor_res
					else:
						vall2=False
					vals1=[]
					vall1=0
					if r[5]!='':
						val1=res = self.pool.get('bc.bom.categorias').name_search(cr, uid, r[5], args=None, operator='ilike', context=None, limit=100)
						vall1=float(val1[0][0]) 
					else:
						vall1=False
					print 'aaaaaaaaa '+str(val)
					if r[6] not in['product','service','consu']:
						raise osv.except_osv(('Atencion!'),("\n El tipo de alguno de los productos es incorrecto"))
					#raise osv.except_osv(('Atencion!'),("\n Desarrollando"))
					if val!=[]:

						#print val
					
						try:
							rellena.append( {
									'product_id' : val[0][0],
									'codigo_producto' : r[0],
									'descripcion_producto' : val[0][1],
									'cantidad':float(r[2]),
									'preciol_unitario':float(r[3]),
									'bom_tipo':r[6],
									'categoria_id':vall1,
									'proveedor_id':vall2 ,
									'cargar': True,
									'stadito':'draft',
							})
						except:
							raise osv.except_osv(('Atencion!'),("\n Elija un archivo en formato CSV y formateado correctamente. O posiblemente deba cambiar el separador de decimales por punto(.) en los montos"))
					else:
						cont+=1
						#print row
						try:
							rellena1.append( {
									'codigo_producto' : r[0],
									'descripcion_producto' : r[1],
									'cantidad':float(r[2]),
									'preciol_unitario':float(r[3]),
									'bom_tipo':r[6],
									
									'categoria_id':vall1,
									'proveedor_id':vall2 ,
									'cargar':False,
									'stadito':'draft',
							})
						except:
							raise osv.except_osv(('Atencion!'),("\n 1Elija un archivo en formato CSV y formateado correctamente. O posiblemente deba cambiar el separador de decimales por punto(.) en los montos"))
							#writer.writerow(row)

			else:
				contt+=1
		#ofile.close()

		#print base64.b64encode(archivo)
		#print binascii.a2b_qp(archivo)
		#print '\n\n\narchi '+str(archivo)+'\n\n\n'
		#print '\n\n\narchi '+str(base64.b64decode(archivo))+'\n\n\n'
		#print {'value':{'bom_equipo_id': rellena}}
		#return {'value':{'bom_equipo_id': rellena}}
		#return self.write(cr, uid, ids, {'bom_equipo_id': rellena},context=context)
		rellena1+=rellena
		return {'value': {'bom_equipo_id': rellena1}}

	#<!--<button name="create_products" string="Crear Faltantes"  icon="terp-camera_test" type="object"/>-->

	def create(self, cr, uid, vals, context=None):
		#print '\n\naaa '+str(vals)+' aaa\n\n bbb '+str(context)+' bbb \n\n'
		#print '\n\n\n\nsegundo'
		
		'''for i in vals['bom_equipo_id']:

			if i[2]!=False:
				#val=self.get_codigo(cr, uid, [0],i[2]['codigo_producto'], context=context)
				print '\n\nvalor   '+str(i[2]['codigo_producto'])
				val = self.pool.get('product.product').name_search(cr, uid, str(i[2]['codigo_producto']), args=None, operator='ilike', context=None, limit=100)
				print '\n\nsdgfsfgfsd   '+str(val)
				if val!=[]:
					i[2]['cargar']=True
					i[2]['product_id']=val[0][0]
				else:
					raise osv.except_osv(('Atencion!'),("\n Existen productos que aun no estan creados! \nPresione 'Crear Faltantes' para añadirlos"))'''
		fila = super(business_case, self).create(cr, uid, vals, context=context)
		return fila
	
	def onchange_oportunidad(self, cr, uid, ids, oportunidad_id, context=None):
		if oportunidad_id==False:
			return True
		model_data=self.pool.get('crm.lead')
		conditions = model_data.search(cr, uid, [('id', '=', oportunidad_id)])
		i = model_data.read(cr, uid, conditions)
		cliente_id=i[0]['partner_id']
		user_id=i[0]['user_id']
		deal_id=i[0]['deal_id']
		model_data=self.pool.get('res.partner')
		conditions = model_data.search(cr, uid, [('id', '=', cliente_id[0])])
		a = model_data.read(cr, uid, conditions)
		telefono_cliente=a[0].get('phone',False)
		direccion_entrega=a[0]['street']
		email_cliente=a[0]['email']
		return {'value': {'cliente_id':cliente_id,'telefono_cliente':telefono_cliente,'direccion_entrega':direccion_entrega,'email_cliente':email_cliente,'user_id':user_id,'deal_fabricantes':deal_id}}
	def boton_validar_bc(self, cr, uid, ids, context=None):	
		bom=self.pool.get('bc.bom.equipo')
		for b in context['bom_equipo_id']:
			bom.write(cr, uid, [b[1]], {'stadito':'sale'})#CHITOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
		self.write(cr, uid, ids, {'state':'sale'})
		
		oppor=self.pool.get('crm.lead')
		#print context['oportunidad_id']
		oppor.write(cr, uid, [context['oportunidad_id']], {'bc_id':ids[0]})
		#if int(context['version'])==1:
		
		compania=self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
		#print "COMPAÑIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA: "+str(compania)
		
		ids1 = self.pool.get('ir.sequence').search(cr, uid, ['&', ('code', '=', 'business.case'), ('company_id', '=', compania)])
		number = self.pool.get('ir.sequence')._next(cr, uid, ids1, context)
		
		
		'''if compania==3:
			number = self.pool.get('ir.sequence').get(cr, uid, 'business.caseCR')
		if compania==9:
			number['number'] = self.pool.get('ir.sequence').get(cr, uid, 'business.caseES')
		if compania==12:
			number['number'] = self.pool.get('ir.sequence').get(cr, uid, 'business.caseGU')
		if compania==11:
			number['number'] = self.pool.get('ir.sequence').get(cr, uid, 'business.caseHO')
		if compania==7:
			<number['number'] = self.pool.get('ir.sequence').get(cr, uid, 'business.caseNI')
		if compania==8:
			number['number'] = self.pool.get('ir.sequence').get(cr, uid, 'business.casePA')'''
		self.write(cr, uid, ids, {'number':number})
		return True
	
	def boton_cancelar_bc(self, cr, uid, ids, context=None):#cancelarrrrrrrrrrrr
		self.write(cr, uid, ids, {'state':'cancel'})
		oppor=self.pool.get('crm.lead')
		oppor.write(cr, uid, [context['oportunidad_id']], {'bc_id':None})
		return True
	
	def crear_productos(self, cr, uid, ids, context=None):
		if ids!=[]:
			print ids
			record = self.browse(cr, uid, ids[0])
			linea = self.pool.get('bc.bom.equipo')
			product = self.pool.get('product.product')
			for i in record.bom_equipo_id:
				if not i.product_id:					
					if i.cargar!=True:
						if i.bom_tipo not in ['product','service','consu']:
							raise osv.except_osv(('Atencion!'),("\n Elija un tipo de producto correcto"))			
						var= product.create(cr,uid,{'name':i.descripcion_producto,'default_code':i.codigo_producto,'type':i.bom_tipo,'type_bom':i.categoria_id.id,'company_id':False},context=None)
						linea.write(cr,uid,[i.id],{'cargar':True, 'product_id' : var}) 
		return True
	def limpiar_bom(self, cr, uid, ids, context=None):
		if ids!=[]:
			bom=self.pool.get('bc.bom.equipo')
			list_ids = bom.search(cr, uid, [('bc_id', '=', ids[0])])
			bom.unlink(cr, uid, list_ids, context=None)
			print list_ids
		return True
	
	def boton_copia_bc(self, cr, uid, ids, context=None):
		bc=self.browse(cr, uid, ids, context=context)[0]
		#print "BC HIJOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO "+str(bc.bc_padre_id)
		version=0
		version_anterior=0
		buscar=0 #BUSCAR EN PADRE O LOS HIJOS
		
		if bc.bc_padre_id:
			model_data=self.pool.get('business.case')
			conditions = model_data.search(cr, uid, [('bc_padre_id', '=', bc.bc_padre_id.id)])
			if conditions!=[]:
				print conditions
				hijos=self.browse(cr, uid, conditions, context=context)
				for h in hijos:
					if h.version>version_anterior:
						version_anterior=h.version
		else:
			model_data=self.pool.get('business.case')
			conditions = model_data.search(cr, uid, [('bc_padre_id', '=', ids[0])])
			if conditions!=[]:
				print conditions
				hijos=self.browse(cr, uid, conditions, context=context)
				for h in hijos:
					if h.version>version_anterior:
						version_anterior=h.version
			else:
				version_anterior=int(context['version'])
		'''
		if bc.bc_padre_id:
			print "REVISOOOOOOOOOOOOOOOO PADRE"
			buscar=bc.bc_padre_id.id
		else:
			buscar=ids[0]
			print "REVISOOOOOOOOOOOOOOOO HIJOS DE IDS"
		model_data=self.pool.get('business.case')
		conditions = model_data.search(cr, uid, [('bc_padre_id', '=', buscar)])
		if conditions!=[]:
			print conditions
			hijos=self.browse(cr, uid, conditions, context=context)
			for h in hijos:
				if h.version>version_anterior:
					version_anterior=h.version
		else:
			version_anterior=int(context['version'])
		'''
		version=version_anterior+1
		#print "VERSIONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN: "+str(version)
		#raise osv.except_osv(('Atencion!'),("\n Desarrollo"))
		d={}
		d.update({'version':version})
		d.update({'state':'draft'})
		d.update({'pedido_venta_validado':'draft'})
		d.update({'pedido_venta':''})
		d.update({'proyecto_id':''})
		d.update({'orden_compra':''})
		if bc.bc_padre_id:
			d.update({'bc_padre_id':bc.bc_padre_id.id})
		else:
			d.update({'bc_padre_id':ids[0]})
		#d.update({'oportunidad_id':''})
		#print"\nPRINTTTTTTTTTTTTTTTTTTTTTT"+str(bc.bom_equipo_id)
		#raise osv.except_osv(('Atencion!'),("\n Desarrollando"))	
		result=self.copy(cr, uid, ids[0], default=d, context=None)
		#cambiar los bom de result, ponerle en draft stadito
		bom_equipo=self.pool.get('bc.bom.equipo')
		conditions_bom = bom_equipo.search(cr, uid, [('bc_id', '=', result)])
		
		#for con in conditions:
		bom_equipo.write(cr, uid, conditions_bom, {'stadito':'draft'})
		
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'dis_BusinessCase', 'view_business_case_form')
		view_id = view_ref and view_ref[1] or False,
		return {
			'type': 'ir.actions.act_window',
			'name': 'Business Case',
			'res_model': 'business.case',
			'res_id': result,
			'view_type': 'form',
			'view_mode': 'form',
			'view_id': view_id,
			'target': 'current',
			'nodestroy': True,
		}
	
	def boton_proyecto_bc(self, cr, uid, ids, context=None):
		v_proyect={}
		valor=False
		for i in self.browse(cr,uid,ids):
			if i.pedido_venta.state=='progress' or i.pedido_venta.state=='shipping_except' or i.pedido_venta.state=='invoice_except' or i.pedido_venta.state=='done':
			#if True:
				v_proyect.update({'name':'PROJECT - '+str(i.name)})
				#v_proyect.update({})
				#v_proyect.update({'user_id':i.user_id.id})
				v_proyect.update({'partner_id':i.cliente_id.id})
				v_proyect.update({'referencia':i.id})
				v_proyect.update({'codigo':'CRC BC-'+str(i.id)})
				v_proyect.update({'total_venta':i.resumen_ingreso_c})
				v_proyect.update({'costo_venta':i.resumen_egreso_c})
				v_proyect.update({'m_disponible':i.resumen_egreso_c})
				v_proyect.update({'simbolo':3})				
				# Ingresado por LJB
				v_proyect.update({'rendimiento_estimado': float(100-((100*i.resumen_egreso_c)/i.resumen_ingreso_c))})

				total_costo_salario = 0.0
				total_costo_cargas_sociales = 0.0
				horas_trabajo = 0
				id_linea=[]
				for h in i.horas_totales_id:
					total_costo_salario += h.total_salario
					total_costo_cargas_sociales += h.cargas_sociales
				for horas in i.horas_id:
					horas_trabajo += horas.horas_trabajo
				
				# Para salarios
				id_linea.append([0,False,{'centro_costo': 21,'subcategoria_rel': 1,'cuenta_gastos': 23,'cantidad': horas_trabajo,'m_asignado': total_costo_salario }])
				# Para cargas sociales
				id_linea.append([0,False,{'centro_costo': 21,'subcategoria_rel': 1,'cuenta_gastos': 24,'cantidad': 1,'m_asignado': total_costo_cargas_sociales }])
				# Para viáticos
				for v in i.viaticos_id:
					print "v.account_id .." + str(v.account_id.id)
					id_linea.append([0,False,{'centro_costo': v.analytic_id.id,'subcategoria_rel': v.sub_categ_id.area_id.id,'cuenta_gastos': v.account_id.id,'cantidad': v.cantidad,'m_asignado': v.total_costo }]) 
				# Para materiales adicionales
				costo_viaticos = 0.0
				cantidad_viaticos = 0.0
				for m in i.adicionales_id:
					costo_viaticos += m.costo_final
					cantidad_viaticos += m.cantidad
					id_linea.append([0,False,{'centro_costo': 21,'subcategoria_rel': m.area_id.id,'cuenta_gastos': 254,'cantidad': cantidad_viaticos,'m_asignado': costo_viaticos, 'detalles':'Materiales Adicionales' }]) 
				# ----------------------------------------
				#CARGA DE LINEA EQUIPOS DEL PROYECTO
				if i.bom_equipo_id!=[]:
					model_data=self.pool.get('bc.areas.especialidad')
					conditions = model_data.search(cr, uid, [('name', '=', 'Implementación')])
					areas = model_data.read(cr, uid, conditions)
					bom_cantidad=0
					bom_costo=0.00
					for record in i.bom_equipo_id:
						bom_cantidad+=record.cantidad
						bom_costo+=record.total_costo
					print bom_cantidad
					print bom_costo
					id_linea.append([0,False,{'centro_costo': 36,'subcategoria_rel':areas[0]['id'], 'cuenta_gastos': 284, 'cantidad':bom_cantidad,'m_asignado':bom_costo,'detalles':'Equipos'}])
				# Subir el BOM Equipo a la ficha de proyectos.	
				equipos = []
				for producto in i.bom_equipo_id:
					equipos.append([0,False,{'product_id': producto.product_id.id, 'proveedor_id': producto.proveedor_id.id, 'cantidad': producto.cantidad, 'descuento': producto.descuento}])		
				v_proyect.update({'equipos_id': equipos})
				# -----------------------------------------------				
				v_proyect.update({'id_linea':id_linea, 'cuenta_salarios': 23, 'cuenta_cargas_sociales': 24})
				print"PROYECTOOOOOOOOOO: "+str(v_proyect)
				valor=self.pool.get('project.project').create(cr,uid,v_proyect,context)
				self.write(cr,uid,i.id,{'proyecto_id':valor},context)
				self.write(cr,uid,i.id,{'state':'done'},context)


				# SUBIR A LA RAMA
				'''view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'project', 'edit_project')
				view_id = view_ref and view_ref[1] or False,
				return {
					'type': 'ir.actions.act_window',
					'name': 'Proyecto',
					'res_model': 'project.project',
					'res_id': valor,
					'view_type': 'form',
					'view_mode': 'form',
					'view_id': view_id,
					'target': 'current',
					'nodestroy': True,
				}'''
				# Llamar el wizard de mensajes
				ir_model_data = self.pool.get('ir.model.data')
				try:
				    template_id = ir_model_data.get_object_reference(cr, uid, 'dis_BusinessCase', 'email_template_edi_businesscase')[1]
				except ValueError:
				    template_id = False
				try:
				    compose_form_id = ir_model_data.get_object_reference(cr, uid, 'dis_BusinessCase', 'view_enviar_mensajes')[1]
				except ValueError:
				    compose_form_id = False 
				ctx = dict(context)
				ctx.update({
				    'default_model': 'business.case',
				    'default_res_id': ids[0],
				    'default_use_template': bool(template_id),
				    'default_template_id': template_id,
				    'default_composition_mode': 'comment',
				})
				return {
				    'type': 'ir.actions.act_window',
				    'view_type': 'form',
				    'view_mode': 'form',
				    'res_model': 'enviar.mensajes',
				    'views': [(compose_form_id, 'form')],
				    'view_id': compose_form_id,
				    'target': 'new',
				    'context': ctx,
				}

			else:
				raise osv.except_osv(('Atencion!'),("\n El Pedido de venta debe estar validado."))	
		return True
	
	def boton_venta_bc(self, cr, uid, ids, context=None):
		
		#model_data=self.pool.get('ir.attachment')
		#conditions = model_data.search(cr, uid, [('res_model', '=', 'business.case'),('res_id','=',ids[0])])
		#i = model_data.read(cr, uid, conditions)
		#print "HOLAAAAAAAAAAAAAAAAAAA: "+str(i)
		#if i!=[]:
		if context['pedido_venta']!=False:
			raise osv.except_osv(('Atencion!'),("\n El Pedido de venta ya fue generado"))
		#print "holaaaaaaaaaaaaa: " +str(self.default_get(cr,uid,['date_order'],context=None))
		model_data=self.pool.get('res.users')
		conditions = model_data.search(cr, uid, [('id', '=', uid)])
		i = model_data.read(cr, uid, conditions)
		compania=i[0]['company_id'][0]
		model_data=self.pool.get('res.company')
		conditions = model_data.search(cr, uid, [('id', '=', compania)])
		o = model_data.read(cr, uid, conditions)
		moneda=o[0]['currency_id'][0]
		model_data=self.pool.get('product.pricelist')
		conditions = model_data.search(cr, uid, [('company_id', '=', compania),('currency_id', '!=', moneda),('active', '=', True)])
		#print "--> conditions: " + str(conditions)
		a = model_data.read(cr, uid, conditions)
		#print "--> a: " + str(a)
		pricelist_id=a[0]['id']
		#print context['partner_id']


		model_data=self.pool.get('bc.bom.equipo')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0])])
		u = model_data.read(cr, uid, conditions)
		#print "uuuuuuuuuuuuuuu: "+str(u)
		order_line=[]
		precio_venta_equipo=0.00
		precio_costo_equipo=0.00
		precio_venta_servicios=0.00
		margen_equipo=0.00
		margen_servicios=0.00
		for l in u:
			precio_venta_equipo=precio_venta_equipo+float(l.get('precio_total',0))
			precio_costo_equipo=precio_costo_equipo+float(l.get('total_costo',0))
			#margen_equipo=margen_equipo+(float(l.get('precio_total',0)-float(l.get('precio_cu',0))))
			#print"BOMMMMMMMMMMMMMMMMMMMMMMMMM: "+str(l)
			#print '\n\nIMPUESTO'+str(l.get('tax_id',0),)+'\n\n'
			linea_pedido = {
					'product_id': l['product_id'][0],
					'name': l['descripcion_producto'],
					'codigo':l['codigo_producto'],
					'product_uom_qty': l['cantidad'],
					#'cost_sin_imp': l['precio_tu']*l['cantidad'],
					#'cost_sin_imp': l['preciol_unitario']*l['cantidad'],
					'available': l['cantidad'],
					#'precio_lista': l['precio_tu'],
					'discount': l.get('descuento',0),
					'tax_id': l.get('tax_id') != [] and [[6, False, l.get('tax_id')]] or [[6, False, []]],
					'margen': l.get('porc_utilidad',0),
					'partner_id1': l.get('proveedor_id',False) and l.get('proveedor_id')[0],
					'price_unit': l['precio_tu'],
					'precio_venta': l['total_costo'],
					'price_unit': l['precio_unitario'],
					'precio_costo': l['precio_cu'],
					'precio_venta': l['total_costo'],#cuando iniciaron con este módulo, pusieron mal los nombres de los campos.
					'precio_lista': l['preciol_unitario'],
					'cost_sin_imp': l['precio_total'],
					'price_subtotal': l['precio_total_ivi'],
					#Falta jalar en presupuesto la categoría
			        
				}
			#print 'LINEAAAAAAAAAAAAAAAAAAAAAAA: '+str(linea_pedido)
			order_line.append([0,False,linea_pedido])
		#HOLA HOLAAAAA
		# Insertar líneas de montos para las áreas.
		areas_productos = self.pool.get('bc.areas.productos')
		# Implementacion
		if float(context['ingreso_implementacion']) != 0:
			ap = areas_productos.search(cr,uid,[('name','=','Implementación')])
			producto = areas_productos.browse(cr,uid,ap,context=None)[0]
			linea_pedido = {
					'product_id': producto.product_id.id,
					'name': 'Servicio de implementación',
					'product_uom_qty': 1,
					'price_unit': float(context['ingreso_implementacion']) ,
					'precio_lista': float(context['ingreso_implementacion']) ,
					'cost_sin_imp': float(context['ingreso_implementacion']) ,
				}
			order_line.append([0,False,linea_pedido])
		# Mantenimientos
		if float(context['ingreso_mantenimientos']) != 0:
			ap = areas_productos.search(cr,uid,[('name','=','Mantenimientos')])
			producto = areas_productos.browse(cr,uid,ap,context=None)[0]
			linea_pedido = {
					'product_id': producto.product_id.id,
					'name': 'Servicio de mantenimiento',
					'product_uom_qty': 1,
					'price_unit': float(context['ingreso_mantenimientos']),
					'precio_lista': float(context['ingreso_mantenimientos']),
					'cost_sin_imp': float(context['ingreso_mantenimientos']),
				}
			order_line.append([0,False,linea_pedido])
		# NOC
		if float(context['ingreso_noc']) != 0:
			ap = areas_productos.search(cr,uid,[('name','=','Soporte')])
			producto = areas_productos.browse(cr,uid,ap,context=None)[0]
			linea_pedido = {
					'product_id': producto.product_id.id,
					'name': 'Servicio de NOC',
					'product_uom_qty': 1,
					'price_unit': float(context['ingreso_noc']),
					'precio_lista': float(context['ingreso_noc']),
					'cost_sin_imp': float(context['ingreso_noc']),
				}
			order_line.append([0,False,linea_pedido])
		# Infraestructura
		if float(context['ingreso_infraestructura']) != 0:
			ap = areas_productos.search(cr,uid,[('name','=','Infraestructura')])
			producto = areas_productos.browse(cr,uid,ap,context=None)[0]
			linea_pedido = {
					'product_id': producto.product_id.id,
					'name': 'Servicio de infraestructura',
					'product_uom_qty': 1,
					'price_unit': float(context['ingreso_infraestructura']) ,
					'precio_lista': float(context['ingreso_infraestructura']) ,
					'cost_sin_imp': float(context['ingreso_infraestructura']) ,
				}
			order_line.append([0,False,linea_pedido])
		# -------------------------------------------
		objeto=self.read(cr,uid,ids,['garantia','vigencia_oferta','condiciones_pago','deal_fabricantes','fecha_entrega_equipos','fecha_entrega_servicios'],{})
		datos_pedido = { 
					'partner_id': context['partner_id'],
					'user_id': context.get('user_id',False),
					'periodo_id': int(ids[0]), 
					'date_order': time.strftime('%Y-%m-%d'), 
					# Campos requeridos por el sistema. 
					'pricelist_id': pricelist_id, 
					'partner_invoice_id': context['partner_id'], 
					'partner_shipping_id': context['partner_id'],
		            		'order_line':order_line,		           
					}
		datos_pedido.update(objeto[0])
		pedido_id=self.pool.get('sale.order').create(cr, uid, datos_pedido, context=context)
		#jeank
		print "precio_venta_equipo: "+str(precio_venta_equipo)
		#raise osv.except_osv(('Atencion!'),("\n Progra."))
		#Escribir datos en Oportunidad
		ingreso_propuesto=self.pool.get('bc.ingreso.propuesto')
		id_ip = ingreso_propuesto.search(cr, uid, [('bc_id', '=', ids[0])])
		ips=ingreso_propuesto.browse(cr, uid, id_ip, context=context)
		for ip in ips:
			precio_venta_servicios=float(precio_venta_servicios)+float(ip.monto_venta)
			
		#Costo de Viáticos
		costo_viaticos=0.00
		ingreso_presupuestado=self.pool.get('bc.ingreso.presupuestado')
		id_ipre = ingreso_presupuestado.search(cr, uid, [('bc_id', '=', ids[0])])
		ipres=ingreso_presupuestado.browse(cr, uid, id_ipre, context=context)
		
		for ipre in ipres:
			if ipre.cdo_id.name=="Costo de Viáticos":
				costo_viaticos=costo_viaticos+ipre.implementacion
				costo_viaticos=costo_viaticos+ipre.mantenimientos
				costo_viaticos=costo_viaticos+ipre.infraestructura
				costo_viaticos=costo_viaticos+ipre.noc
		#jeank_lunes
		margen_servicios=precio_venta_servicios-costo_viaticos
		#raise osv.except_osv(('Atencion!'),("\n Progra."))
		margen_equipo=precio_venta_equipo-precio_costo_equipo
		oppor=self.pool.get('crm.lead')
		oppor.write(cr, uid, [context['oportunidad_id']], {'precio_venta_equipo':precio_venta_equipo,'precio_venta_servicios':precio_venta_servicios,'planned_revenue':precio_venta_equipo+precio_venta_servicios,'margen_equipo':margen_equipo,'margen_servicios':margen_servicios,'margen_total':margen_equipo+margen_servicios})
		self.write(cr, uid, ids, {'pedido_venta':pedido_id})
		'''#self.write(cr, uid, ids, {'state':'done'})'''
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'view_order_form')
		view_id = view_ref and view_ref[1] or False,
		return {
			'type': 'ir.actions.act_window',
			'name': 'Pedido de Venta',
			'res_model': 'sale.order',
			'res_id': pedido_id,
			'view_type': 'form',
			'view_mode': 'form',
			'view_id': view_id,
			'target': 'current',
			'nodestroy': True,
		}
		#else:
		#	raise osv.except_osv(('Atencion!'),("\n Debe adjuntar la orden de compra externa."))
		#	return True
	def todos_los_botones(self, cr, uid, ids, context=None):
		#print"CONTEXTTTTTTTTTTTTTTT: "+str(context)
		self.boton_actualizar_horas_trabajo(cr, uid, ids, context=context)
		self.boton_actualizar_viaticos(cr, uid, ids, context=context)
		self.boton_actualizar_adicionales(cr, uid, ids, context=context)
		self.boton_actualizar_ingreso_propuesto(cr, uid, ids, context=context)
		self.boton_actualizar_margen(cr, uid, ids, context=context)
		#REVISAR: HAY QUE HACERLO 2 VECES PARA VER LOS CAMBIOS (ORDENAR METODOS)
		self.boton_actualizar_horas_trabajo(cr, uid, ids, context=context)
		self.boton_actualizar_viaticos(cr, uid, ids, context=context)
		self.boton_actualizar_adicionales(cr, uid, ids, context=context)
		self.boton_actualizar_ingreso_propuesto(cr, uid, ids, context=context)
		self.boton_actualizar_margen(cr, uid, ids, context=context)
		return True
	
	def boton_actualizar_ingreso_propuesto(self, cr, uid, ids, context=None):
		#SUMA DE COSTOS DE IMPLEMENTACION
		#################################
		implementacion_ip_por=0.00
		mantenimientos_ip_por=0.00
		infra_ip_por=0.00
		noc_ip_por=0.00
		for u in context['ingreso_p']:
			model_data=self.pool.get('bc.ingreso.propuesto')
			conditions = model_data.search(cr, uid, [('id', '=', u[1])])
			e = model_data.read(cr, uid, conditions)
			#print "INGRESO PROPUESTO SUPERIOR: "+str(e)
			#print "PORRRRRRRRRRRRRRRRRR: "+str(e[0]['area_id'])
			if e[0]['area_id'][1]=="Implementación":
				implementacion_ip_por=e[0]['porc_venta']
				#print "PORRRRRRRRRRRRRRRRRR: "+str(por_implementacion)
			if e[0]['area_id'][1]=="Mantenimiento":
				mantenimientos_ip_por=e[0]['porc_venta']
			if e[0]['area_id'][1]=="Infraestructura":
				infra_ip_por=e[0]['porc_venta']
			if e[0]['area_id'][1]=="NOC":
				noc_ip_por=e[0]['porc_venta']
		#################################
		model_data=self.pool.get('bc.ingreso.presupuestado')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0])])
		i = model_data.read(cr, uid, conditions)
		
		#print "CONTEXTTTTTTTTTTTTT: "+str(context)
		implementacion_costo=0
		mantenimientos_costo=0
		infra_costo=0
		noc_costo=0
		
		implementacion_ip=0
		mantenimientos_ip=0
		infra_ip=0
		noc_ip=0
		
		implementacion_margen=0
		mantenimientos_margen=0
		infra_margen=0
		noc_margen=0
		ingreso_total=0.00
		#CALCULOS
		for x in i:
			implementacion_costo+=float(x['implementacion'])
			mantenimientos_costo+=float(x['mantenimientos'])
			infra_costo+=float(x['infraestructura'])
			noc_costo+=float(x['noc'])
			#print "NOC COSTO ... " + str(noc_costo)
			
		if 1-float(implementacion_ip_por)!=0:
			implementacion_ip=implementacion_costo/(1-(float(implementacion_ip_por)*0.01))
		if 1-float(mantenimientos_ip_por)!=0:
			mantenimientos_ip=mantenimientos_costo/(1-(float(mantenimientos_ip_por)*0.01))
		if 1-float(infra_ip_por)!=0:
			infra_ip=infra_costo/(1-(float(infra_ip_por)*0.01))
		if 1-float(noc_ip_por)!=0:
			noc_ip=noc_costo/(1-(float(noc_ip_por)*0.01))
			
		#implementacion_margen=implementacion_ip*(float(context['implementacion_margen_por'])*0.01)
		#mantenimientos_margen=mantenimientos_ip*(float(context['mantenimientos_margen_por'])*0.01)
		#infra_margen=infra_ip*(float(context['infra_margen_por'])*0.01)
		#noc_margen=noc_ip*(float(context['noc_margen_por'])*0.01)

		# Obtener los porcentajes del margen de contribucion 
		objeto = self.pool.get('bc.margen.contribucion')
		
		
		#NUEVO CALCULO DE MARGEN DE CONTRIBUCION
		implementacion_ip2=0.00
		mantenimientos_ip2=0.00
		infra_ip2=0.00
		noc_ip2=0.00
		ingreso_p=self.pool.get('bc.ingreso.propuesto')
		id_ip = ingreso_p.search(cr, uid, [('bc_id', '=', ids[0])])
		ipropuestos=ingreso_p.browse(cr, uid, id_ip, context=context)
		for ipropuesto in ipropuestos:
			if ipropuesto.area_id.name=="Implementación":
				implementacion_ip2=implementacion_ip2+ipropuesto.monto_venta
			if ipropuesto.area_id.name=="Mantenimiento":
				mantenimientos_ip2=mantenimientos_ip2+ipropuesto.monto_venta
			if ipropuesto.area_id.name=="Infraestructura":
				infra_ip2=infra_ip2+ipropuesto.monto_venta
			if ipropuesto.area_id.name=="NOC":
				noc_ip2=noc_ip2+ipropuesto.monto_venta
				
		ingreso_p=self.pool.get('bc.ingreso.presupuestado')
		id_ip = ingreso_p.search(cr, uid, [('bc_id', '=', ids[0])])
		ipropuestos=ingreso_p.browse(cr, uid, id_ip, context=context)
		for ipropuesto in ipropuestos:
			if ipropuesto.cdo_id.name=="Costo de Viáticos":
				implementacion_ip2=implementacion_ip2-ipropuesto.implementacion
				mantenimientos_ip2=mantenimientos_ip2-ipropuesto.mantenimientos
				infra_ip2=infra_ip2-ipropuesto.infraestructura
				noc_ip2=noc_ip2-ipropuesto.noc
				
		########################################
		
		conditions = objeto.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Implementación')])
		i = objeto.read(cr, uid, conditions)
		implementacion_margen=implementacion_ip2*(float(i[0]['porc_contribucion'])*0.01)
		
		conditions = objeto.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Mantenimiento')])
		i = objeto.read(cr, uid, conditions)
		#mantenimientos_margen=mantenimientos_ip*(float(context['mantenimientos_margen_por'])*0.01)
		mantenimientos_margen=mantenimientos_ip2*(float(i[0]['porc_contribucion'])*0.01)
		
		conditions = objeto.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Infraestructura')])
		i = objeto.read(cr, uid, conditions)
		#infra_margen=infra_ip*(float(context['infra_margen_por'])*0.01)
		infra_margen=infra_ip2*(float(i[0]['porc_contribucion'])*0.01)
		
		conditions = objeto.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','NOC')])
		i = objeto.read(cr, uid, conditions)
		#noc_margen=noc_ip*(float(context['noc_margen_por'])*0.01)
		noc_margen=noc_ip2*(float(i[0]['porc_contribucion'])*0.01)

		#ESCRITURAS
		model_data=self.pool.get('bc.costo.operacion')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Implementación')])
		i = model_data.read(cr, uid, conditions)
		model_data.write(cr, uid, i[0]['id'], {'monto_costo':implementacion_costo})
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Mantenimiento')])
		i = model_data.read(cr, uid, conditions)
		model_data.write(cr, uid, i[0]['id'], {'monto_costo':mantenimientos_costo})
		#self.write(cr, uid, ids, {'mantenimientos_costo':mantenimientos_costo})
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Infraestructura')])
		i = model_data.read(cr, uid, conditions)
		model_data.write(cr, uid, i[0]['id'], {'monto_costo':infra_costo})
		#self.write(cr, uid, ids, {'infra_costo':infra_costo})
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','NOC')])
		i = model_data.read(cr, uid, conditions)
		model_data.write(cr, uid, i[0]['id'], {'monto_costo':noc_costo})
		#self.write(cr, uid, ids, {'noc_costo':noc_costo})
		
		model_data=self.pool.get('bc.ingreso.propuesto')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Implementación')])
		i = model_data.read(cr, uid, conditions)
		model_data.write(cr, uid, i[0]['id'], {'monto_venta':implementacion_ip})
		self.write(cr, uid, ids, {'implementacion_ip':implementacion_ip})

		self.write(cr, uid, ids, {'ingreso_implementacion':implementacion_ip})#MARGEN DE OPERACION
		if implementacion_ip!=0:
			self.write(cr, uid, ids, {'porc_ingreso_implementacion':implementacion_ip_por})

		model_data=self.pool.get('bc.ingreso.propuesto')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Mantenimiento')])
		i = model_data.read(cr, uid, conditions)
		model_data.write(cr, uid, i[0]['id'], {'monto_venta':mantenimientos_ip})
		self.write(cr, uid, ids, {'mantenimientos_ip':mantenimientos_ip})

		self.write(cr, uid, ids, {'ingreso_mantenimientos':mantenimientos_ip})#MARGEN DE OPERACION
		if mantenimientos_ip!=0:
			self.write(cr, uid, ids, {'porc_ingreso_mantenimientos':mantenimientos_ip_por})

		model_data=self.pool.get('bc.ingreso.propuesto')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Infraestructura')])
		i = model_data.read(cr, uid, conditions)
		model_data.write(cr, uid, i[0]['id'], {'monto_venta':infra_ip})
		self.write(cr, uid, ids, {'infra_ip':infra_ip})

		self.write(cr, uid, ids, {'ingreso_infraestructura':infra_ip})#MARGEN DE OPERACION
		if infra_ip!=0:
			self.write(cr, uid, ids, {'porc_ingreso_infraestructura':infra_ip_por})
		
		model_data=self.pool.get('bc.ingreso.propuesto')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','NOC')])
		i = model_data.read(cr, uid, conditions)
		model_data.write(cr, uid, i[0]['id'], {'monto_venta':noc_ip})
		self.write(cr, uid, ids, {'noc_ip':noc_ip})

		self.write(cr, uid, ids, {'ingreso_noc':noc_ip})#MARGEN DE OPERACION
		if noc_ip!=0:
			self.write(cr, uid, ids, {'porc_ingreso_noc':noc_ip_por})
		

		model_data=self.pool.get('bc.margen.contribucion')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Implementación')])
		i = model_data.read(cr, uid, conditions)
		model_data.write(cr, uid, i[0]['id'], {'monto_contribucion':implementacion_margen})
		#self.write(cr, uid, ids, {'implementacion_margen':implementacion_margen})
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Mantenimiento')])
		i = model_data.read(cr, uid, conditions)
		model_data.write(cr, uid, i[0]['id'], {'monto_contribucion': mantenimientos_margen})
		#self.write(cr, uid, ids, {'mantenimientos_margen':mantenimientos_margen})
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Infraestructura')])
		i = model_data.read(cr, uid, conditions)
		model_data.write(cr, uid, i[0]['id'], {'monto_contribucion':infra_margen})
		#self.write(cr, uid, ids, {'infra_margen':infra_margen})
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','NOC')])
		i = model_data.read(cr, uid, conditions)
		model_data.write(cr, uid, i[0]['id'], {'monto_contribucion':noc_margen})
		#self.write(cr, uid, ids, {'noc_margen':noc_margen})
		
		
		
		total_venta=0.00
		cargas_sociales=0.00
		model_data=self.pool.get('bc.totales.horas')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0])])
		i = model_data.read(cr, uid, conditions)
		for a in i:
			####SALARIOS
			if a['area_id'][1]=="Implementación":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Salarios')])
				o = model_data.read(cr, uid, conditions)
				total_venta=float(a['total_salario'])
				model_data.write(cr, uid, o[0]['id'], {'implementacion':total_venta})
			if a['area_id'][1]=="Mantenimiento":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Salarios')])
				o = model_data.read(cr, uid, conditions)
				total_venta=float(a['total_salario'])
				model_data.write(cr, uid, o[0]['id'], {'mantenimientos':total_venta})
			if a['area_id'][1]=="Infraestructura":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Salarios')])
				o = model_data.read(cr, uid, conditions)
				total_venta=float(a['total_salario'])
				model_data.write(cr, uid, o[0]['id'], {'infraestructura':total_venta})
			if a['area_id'][1]=="NOC":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Salarios')])
				o = model_data.read(cr, uid, conditions)
				total_venta=float(a['total_salario'])
				model_data.write(cr, uid, o[0]['id'], {'noc':total_venta})
				
			####Cargas Sociales
			if a['area_id'][1]=="Implementación":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Cargas Sociales')])
				o = model_data.read(cr, uid, conditions)
				cargas_sociales=float(a['cargas_sociales'])
				model_data.write(cr, uid, o[0]['id'], {'implementacion':cargas_sociales})
			if a['area_id'][1]=="Mantenimiento":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Cargas Sociales')])
				o = model_data.read(cr, uid, conditions)
				cargas_sociales=float(a['cargas_sociales'])
				model_data.write(cr, uid, o[0]['id'], {'mantenimientos':cargas_sociales})
			if a['area_id'][1]=="Infraestructura":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Cargas Sociales')])
				o = model_data.read(cr, uid, conditions)
				cargas_sociales=float(a['cargas_sociales'])
				model_data.write(cr, uid, o[0]['id'], {'infraestructura':cargas_sociales})
			if a['area_id'][1]=="NOC":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Cargas Sociales')])
				o = model_data.read(cr, uid, conditions)
				cargas_sociales=float(a['cargas_sociales'])
				model_data.write(cr, uid, o[0]['id'], {'noc':cargas_sociales})
		
		
		total_viaticos=0.00
		model_data=self.pool.get('bc.totales.viaticos')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0])])
		i = model_data.read(cr, uid, conditions)
		for a in i:
			if a['sub_categoria_id'][1]=="Implementación":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Costo de Viáticos')])
				o = model_data.read(cr, uid, conditions)
				total_viaticos=float(a['total_costo_viaticos'])
				model_data.write(cr, uid, o[0]['id'], {'implementacion':total_viaticos})
			if a['sub_categoria_id'][1]=="Mantenimiento":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Costo de Viáticos')])
				o = model_data.read(cr, uid, conditions)
				total_viaticos=float(a['total_costo_viaticos'])
				model_data.write(cr, uid, o[0]['id'], {'mantenimientos':total_viaticos})
			if a['sub_categoria_id'][1]=="Infraestructura":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Costo de Viáticos')])
				o = model_data.read(cr, uid, conditions)
				total_viaticos=float(a['total_costo_viaticos'])
				model_data.write(cr, uid, o[0]['id'], {'infraestructura':total_viaticos})
			if a['sub_categoria_id'][1]=="NOC":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Costo de Viáticos')])
				o = model_data.read(cr, uid, conditions)
				total_viaticos=float(a['total_costo_viaticos'])
				model_data.write(cr, uid, o[0]['id'], {'noc':total_viaticos})
					
		total_materiales=0.00
		model_data=self.pool.get('bc.totales.adicionales')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0])])
		i = model_data.read(cr, uid, conditions)
		for a in i:
			if a['area_id'][1]=="Implementación":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Materiales Adicionales')])
				o = model_data.read(cr, uid, conditions)
				total_materiales=float(a['total_costo_materiales'])
				model_data.write(cr, uid, o[0]['id'], {'implementacion':total_materiales})
			if a['area_id'][1]=="Mantenimiento":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Materiales Adicionales')])
				o = model_data.read(cr, uid, conditions)
				total_materiales=float(a['total_costo_materiales'])
				model_data.write(cr, uid, o[0]['id'], {'mantenimientos':total_materiales})
			if a['area_id'][1]=="Infraestructura":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Materiales Adicionales')])
				o = model_data.read(cr, uid, conditions)
				total_materiales=float(a['total_costo_materiales'])
				model_data.write(cr, uid, o[0]['id'], {'infraestructura':total_materiales})
			if a['area_id'][1]=="NOC":
				model_data=self.pool.get('bc.ingreso.presupuestado')
				conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0]),('cdo_id','=','Materiales Adicionales')])
				o = model_data.read(cr, uid, conditions)
				total_materiales=float(a['total_costo_materiales'])
				model_data.write(cr, uid, o[0]['id'], {'noc':total_materiales})
		
		return True
	
	def boton_actualizar_horas_trabajo(self, cr, uid, ids, context=None):
		
		model_data=self.pool.get('bc.totales.horas')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0])])
		e = model_data.read(cr, uid, conditions)
		
		total_horas=0.00
		total_fte=0.00
		total_salario=0.00
		cargas_sociales=0.00
		total_costo_horas=0.00
		total_venta_horas=0.00
		for a in e:
			total_horas=0.00
			total_fte=0.00
			total_salario=0.00
			cargas_sociales=0.00
			total_costo_horas=0.00
			total_venta_horas=0.00
			model_data=self.pool.get('bc.horas')
			conditions = model_data.search(cr, uid, [('bc_id','=', ids[0]),('area_id', '=', a['area_id'][0] )])
			i = model_data.read(cr, uid, conditions)
			#print i
			objeto = self.pool.get('bc.ingreso.propuesto')
			for o in i:
				total_horas=total_horas+float(o['horas_trabajo'])*float(o.get('cadencia',1))*float(o.get('numero_personas',1))
				total_fte=total_fte+float(o['cantidad_fte'])
				total_salario=total_salario+float(o['salario'])
				cargas_sociales=cargas_sociales+float(o['cargas_sociales'])
				total_costo_horas=float(total_salario)+float(cargas_sociales)
				
				if o['area_id'][1]=="Implementación":
					conditions = objeto.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Implementación')])
					i = objeto.read(cr, uid, conditions)
					#if (1-float(context['implementacion_ip_por']))!=0:
					if (1-float(i[0]['porc_venta'])) != 0 :
						total_venta_horas=float(total_costo_horas)/((1-float(i[0]['porc_venta'])*0.01)) #hacer los if directos if variable=Implementación:
						#print 'aa'+str(total_venta_horas)
				if o['area_id'][1]=="Mantenimiento":
					conditions = objeto.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Mantenimiento')])
					i = objeto.read(cr, uid, conditions)
					#if (1-float(context['mantenimientos_ip_por']))!=0:
					if (1-float(i[0]['porc_venta'])) != 0 :
						total_venta_horas=float(total_costo_horas)/((1-float(i[0]['porc_venta'])*0.01)) #hacer los if directos if variable=Implementación:
				if o['area_id'][1]=="Infraestructura":
					conditions = objeto.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','Infraestructura')])
					i = objeto.read(cr, uid, conditions)
					#if (1-float(context['infra_ip_por']))!=0:
					if (1-float(i[0]['porc_venta'])) != 0 :
						total_venta_horas=float(total_costo_horas)/((1-float(i[0]['porc_venta'])*0.01)) #hacer los if directos if variable=Implementación:
				if o['area_id'][1]=="NOC":
					conditions = objeto.search(cr, uid, [('bc_id', '=', ids[0]),('area_id','=','NOC')])
					i = objeto.read(cr, uid, conditions)
					#if (1-float(context['noc_ip_por']))!=0:
					if (1-float(i[0]['porc_venta'])) != 0 :
						total_venta_horas=float(total_costo_horas)/((1-float(i[0]['porc_venta'])*0.01)) #hacer los if directos if variable=Implementación:
			#print 'mm'+str(total_venta_horas)
			self.pool.get('bc.totales.horas').write(cr, uid, a['id'], {'total_horas': total_horas,'total_fte': total_fte, 'total_salario': total_salario, 'cargas_sociales': cargas_sociales, 'total_costo_horas': total_costo_horas, 'total_venta_horas': total_venta_horas})
		return True
	
	def boton_actualizar_viaticos(self, cr, uid, ids, context=None):
		'''model_data=self.pool.get('bc.totales.viaticos')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0])])
		e = model_data.read(cr, uid, conditions)

		total_costo_viaticos=0.00
		total_venta_viaticos=0.00
		for a in e:
			total_costo_viaticos=0.00
			total_venta_viaticos=0.00
			model_data=self.pool.get('bc.viaticos')
			br_conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0])])
			br = model_data.browse(cr, uid, br_conditions)[0]
			print "BRRRRRRRRRRRRRRRRRRRRRRRRRRRR \n"+str(br.sub_categ_id.area_id.name)
			if br.sub_categ_id.area_id.id==a['sub_categoria_id']:
				conditions = model_data.search(cr, uid, [('bc_id','=', ids[0]),('sub_categ_id', '=', br.sub_categ_id.id)])
				i = model_data.read(cr, uid, conditions)
				#print i
				for o in i:
					total_costo_viaticos=float(total_costo_viaticos)+float(o['total_costo'])
					total_venta_viaticos=float(total_venta_viaticos)+float(o['total_venta'])
				self.pool.get('bc.totales.viaticos').write(cr, uid, a['id'], {'total_costo_viaticos': total_costo_viaticos, 'total_venta_viaticos': total_venta_viaticos})
		'''
		
		id_lines={}
		for i in self.browse(cr, uid, ids):
			for j in i.totales_viaticos_id:
				id_lines.update({j.sub_categoria_id.id:{'total_costo_viaticos':0.00,'total_venta_viaticos':0.00}})
		vec={}
		sum1=0
		sum2=0
		for i in self.browse(cr, uid, ids):
			for j in i.viaticos_id:
				val=j.sub_categ_id.area_id.id
				if val !=None and val!=False:
					id_lines.get(val)['total_costo_viaticos']+=j.total_costo
					id_lines.get(val)['total_venta_viaticos']+=j.total_venta
		bb=self.pool.get('bc.totales.viaticos')
		for i in id_lines:
			idss= bb.search(cr, uid, [('bc_id', '=', ids[0]),('sub_categoria_id','=',i)])
			bb.write(cr,uid,idss,id_lines.get(i),context)
		return True
	
	def boton_actualizar_adicionales(self, cr, uid, ids, context=None):
		model_data=self.pool.get('bc.totales.adicionales')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0])])
		e = model_data.read(cr, uid, conditions)
		
		total_costo_adicionales=0.00
		total_venta_adicionales=0.00
		for a in e:
			total_costo_adicionales=0.00
			total_venta_adicionales=0.00
			model_data=self.pool.get('bc.materiles.adicionales')
			conditions = model_data.search(cr, uid, [('bc_id','=', ids[0]),('area_id', '=', a['area_id'][0] )])
			i = model_data.read(cr, uid, conditions)
			for o in i:
				total_costo_adicionales=float(total_costo_adicionales)+float(o['costo_final'])
				total_venta_adicionales=float(total_venta_adicionales)+float(o['venta_final'])
			self.pool.get('bc.totales.adicionales').write(cr, uid, a['id'], {'total_costo_materiales': total_costo_adicionales, 'total_venta_materiales': total_venta_adicionales})
		return True
	
	def boton_actualizar_margen(self, cr, uid, ids, context=None):
		res = {}
		total_monto_implementacion = 0.00
		total_monto_mantenimientos = 0.00
		total_monto_infraestructura = 0.00 
		total_monto_noc = 0.00
		total_monto_total = 0.00

		model_data=self.pool.get('bc.bom.equipo')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0])])
		e = model_data.read(cr, uid, conditions)

		ingreso_equipos=0.00
		costo=0.00
		porc_ingreso_equipos=0.00
		ingreso_total=0.00
		for a in e:
			if a['cargar']==True:
				ingreso_equipos=float(ingreso_equipos)+float(a['precio_total'])
				costo=float(costo)+float(a['total_costo'])
		if ingreso_equipos!=0:
			porc_ingreso_equipos=1-(float(costo)/float(ingreso_equipos))
		ingreso_total=float(context['ingreso_implementacion'])+float(context['ingreso_mantenimientos'])+float(context['ingreso_noc'])+float(context['ingreso_infraestructura']) + float(ingreso_equipos)
		self.write(cr, uid, ids[0], {'ingreso_equipos': ingreso_equipos, 'porc_ingreso_equipos':porc_ingreso_equipos, 'ingreso_total':ingreso_total})
		
		# De donde tomamos los datos para los Costos Directos de Operacion
		model_data1=self.pool.get('bc.ingreso.presupuestado')
		conditions = model_data1.search(cr, uid, [('bc_id', '=', ids[0])])
		e = model_data1.read(cr, uid, conditions)
		# Donde escribimos los datos para los Costos Directos de Operacion
		model_data2=self.pool.get('bc.margen.operacion')
		conditions = model_data2.search(cr, uid, [('bc_id', '=', ids[0])])
		f = model_data2.read(cr, uid, conditions)
		for data1 in e:
			for data2 in f:
				if data2['name'][1] == data1['cdo_id'][1]:
					suma_montos = float(data1['implementacion']) + float(data1['mantenimientos']) + float(data1['infraestructura']) + float(data1['noc'])
					res = {
						'monto_implementacion': float(data1['implementacion']),
						'monto_mantenimientos': float(data1['mantenimientos']), 
						'monto_infraestructura': float(data1['infraestructura']), 
						'monto_noc': float(data1['noc']), 
						'monto_total': suma_montos,
					      }
					# Por linea coincidida
					model_data2.write(cr, uid, data2['id'], res ,context=context)
					# Para totales en costos de operacion
					total_monto_implementacion += float(data1['implementacion'])
					total_monto_mantenimientos += float(data1['mantenimientos'])
					total_monto_infraestructura += float(data1['infraestructura'])
					total_monto_noc += float(data1['noc'])
					total_monto_total += suma_montos
					
		# Para equipos
		if data2['name'][1] == 'Equipos':
			model_data2.write(cr, uid, data2['id'], {'monto_equipos': costo, 'monto_total': costo },context=context)
		# Escribir los costos de operacion
		costo_total = total_monto_total+costo
		porc_costo_implementacion = 0.00
		porc_costo_mantenimientos = 0.00
		porc_costo_noc = 0.00
		porc_costo_infraestructura = 0.00
		porc_costo_equipos = 0.00 
		porc_costo_total = 0.00
		if total_monto_implementacion != 0 and float(context['ingreso_implementacion']) != 0:
			porc_costo_implementacion = float(float(total_monto_implementacion)/float(context['ingreso_implementacion']))*100.00
		if total_monto_mantenimientos != 0 and float(context['ingreso_mantenimientos']) != 0:
			porc_costo_mantenimientos = float(float(total_monto_mantenimientos)/float(context['ingreso_mantenimientos']))*100.00
		if total_monto_noc != 0 and float(context['ingreso_noc']) != 0:
			porc_costo_noc = float(float(total_monto_noc)/float(context['ingreso_noc']))*100.00
		if total_monto_infraestructura != 0 and float(context['ingreso_infraestructura']) != 0:
			porc_costo_infraestructura = float(float(total_monto_infraestructura)/float(context['ingreso_infraestructura']))*100.00
		if costo != 0 and float(ingreso_equipos) != 0:
			porc_costo_equipos = float(float(costo)/float(ingreso_equipos))*100.00
		if costo_total != 0 and float(ingreso_total) != 0:
			porc_costo_total = float(float(costo_total)/float(ingreso_total))*100.00
		dic = {}
		dic = {
			'costo_implementacion': total_monto_implementacion, 
			'porc_costo_implementacion': porc_costo_implementacion,	
			'costo_mantenimientos': total_monto_mantenimientos, 
			'porc_costo_mantenimientos': porc_costo_mantenimientos,		
			'costo_noc': total_monto_noc, 
			'porc_costo_noc': porc_costo_noc,
			'costo_infraestructura': total_monto_infraestructura, 
			'porc_costo_infraestructura': porc_costo_infraestructura,
			'costo_equipos': costo, 
			'porc_costo_equipos': porc_costo_equipos,
			'costo_total': costo_total, 
			'porc_costo_total': porc_costo_total,
		}
		self.write(cr, uid, ids, dic, context=context)

		# Para Numero de FTE
		total_implementacion_fte =0.00
		total_mantenimientos_fte =0.00
		total_noc_fte =0.00
		total_infraestructura_fte =0.00
		model_data=self.pool.get('bc.horas')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0])])
		i = model_data.read(cr, uid, conditions)
		for a in i:
			if a['area_id'][1]=="Implementación":
				total_implementacion_fte += float(a['cantidad_fte'])
			if a['area_id'][1]=="Mantenimiento":
				total_mantenimientos_fte += float(a['cantidad_fte'])
			if a['area_id'][1]=="Infraestructura":
				total_infraestructura_fte += float(a['cantidad_fte'])
			if a['area_id'][1]=="NOC":
				total_noc_fte += float(a['cantidad_fte'])
		fte_total_calc = float(total_implementacion_fte+total_mantenimientos_fte+total_noc_fte+total_infraestructura_fte)
		self.write(cr, uid, ids, {'fte_implementacion': total_implementacion_fte, 'fte_mantenimientos': total_mantenimientos_fte, 'fte_noc': total_noc_fte, 'fte_infraestructura': total_infraestructura_fte, 'fte_total': fte_total_calc}, context=context)

		# Para indicadores
		model_data=self.pool.get('bc.montos.indicadores')
		conditions = model_data.search(cr, uid, [('bc_id', '=', ids[0])])
		i = model_data.read(cr, uid, conditions)
		res={}
		indicar_implementacion = 0.00
		indicar_mantenimientos = 0.00
		indicar_noc = 0.00
		indicar_infraestructura = 0.00
		indicar_equipos = 0.00
		indicar_total = 0.00
		indicar_implementacion = float(float(context['ingreso_implementacion'])-float(total_monto_implementacion))
		indicar_mantenimientos = float(float(context['ingreso_mantenimientos'])-float(total_monto_mantenimientos))
		indicar_noc = float(float(context['ingreso_noc'])-float(total_monto_noc))
		indicar_infraestructura = float(float(context['ingreso_infraestructura'])-float(total_monto_infraestructura))
		indicar_equipos = float(float(ingreso_equipos)-float(costo))
		indicar_total = float(float(ingreso_total)-float(costo_total))
		for ln in i:
			if str(ln['name'][1]) == "Margen de Operación" :
				res ={
					'indicador_implementacion': float(indicar_implementacion),
					'indicador_mantenimientos': float(indicar_mantenimientos),
					'indicador_noc': indicar_noc,
					'indicador_infraestructura': indicar_infraestructura,
					'indicador_equipos': indicar_equipos,
					'indicador_total': indicar_total,
				}
				model_data.write(cr, uid, ln['id'], res, context=context)
			elif str(ln['name'][1]) == "Porcentaje de Contribución" :
				ingreso_implementacion = 0.00
				ingreso_mantenimientos = 0.00
				ingreso_noc = 0.00
				ingreso_infraestructura = 0.00
				ingresos_equipos = 0.00
				ingresos_total = 0.00
				# Validar que las divisiones no sean entre 0 
				if float(context['ingreso_implementacion']) != 0:
					ingreso_implementacion = float(indicar_implementacion/float(context['ingreso_implementacion']))*100.00
				if float(context['ingreso_mantenimientos']) != 0:
					ingreso_mantenimientos = float(indicar_mantenimientos/float(context['ingreso_mantenimientos']))*100.00
				if float(context['ingreso_noc']) != 0:	
					ingreso_noc = float(indicar_noc/float(context['ingreso_noc']))*100.00
				if float(context['ingreso_infraestructura']) != 0:	
					ingreso_infraestructura = float(indicar_infraestructura/float(context['ingreso_infraestructura']))*100.00
				if float(ingreso_equipos) != 0:
					ingresos_equipos = float(indicar_equipos/float(ingreso_equipos))*100.00	
				if float(ingreso_total) != 0:
					ingresos_total = float(indicar_total/float(ingreso_total))*100.00
				res ={
					'indicador_implementacion': ingreso_implementacion,
					'indicador_mantenimientos': ingreso_mantenimientos,
					'indicador_noc': ingreso_noc,
					'indicador_infraestructura': ingreso_infraestructura,
					'indicador_equipos': ingresos_equipos,
					'indicador_total': ingresos_total,
				}
				model_data.write(cr, uid, ln['id'], res, context=context)
			elif str(ln['name'][1]) == "Contribución por FTE" :
				fte_implementacion = 0.00
				fte_mantenimientos = 0.00
				fte_noc = 0.00
				fte_infraestructura = 0.00
				# Validar que las divisiones no sean entre 0 
				if float(total_implementacion_fte) != 0:
					fte_implementacion = indicar_implementacion/total_implementacion_fte
				if float(total_mantenimientos_fte) != 0:
					fte_mantenimientos = indicar_mantenimientos/total_mantenimientos_fte
				if float(total_noc_fte) != 0:	
					fte_noc = indicar_noc/total_noc_fte
				if float(total_infraestructura_fte) != 0:	
					fte_infraestructura = indicar_infraestructura/total_infraestructura_fte
				res ={
					'indicador_implementacion': fte_implementacion,
					'indicador_mantenimientos': fte_mantenimientos,
					'indicador_noc': fte_noc,
					'indicador_infraestructura': fte_infraestructura,
					'indicador_equipos': 0.00,
					'indicador_total': 0.00,
				}
				model_data.write(cr, uid, ln['id'], res, context=context)
		# Se escribe el último valor de total porcentaje en ingreso propuesto.
		self.write(cr, uid, ids[0], {'porc_ingreso_total': ingresos_total, 'resumen_ingreso': ingreso_total, 'resumen_egreso': costo_total, 'resumen_utilidad': indicar_total, 'resumen_ingreso_c': ingreso_total, 'resumen_egreso_c': costo_total, 'resumen_utilidad_c': indicar_total}, context=context)
		return True
	
	def onchange_cliente(self, cr, uid, ids, cliente_id, context=None):
	  
		#datos = self.pool.get('res.partner').browse(cr, uid, cliente_id, context=context)
		#print "\n\n"+str(datos.child_ids)+"\n\n"
		name = ''
		phone = ''
		street = ''
		email = ''
		contactos_id = []
		#print "\n\n"+str(contactos_id)+"\n\n"
		for datos in self.pool.get('res.partner').read(cr,uid,[cliente_id],context=None):
			print "\n\n"+str(datos)+"\n\n"
			name = datos['name']
			phone = datos['phone']
			street = datos['street']
			email = datos['email']
			contactos_id = datos['child_ids']
		return {'value': {'contactos_id':contactos_id, 'telefono_cliente': phone, 'direccion_entrega': street, 'email_cliente': email}}
	  
business_case()

# Campos y funciones para las aprobaciones que se mostrarán en la pestaña de Generalidades del BC.
class bc_aprobaciones(osv.osv):

	_name = 'bc.aprobaciones'
	_columns = {
	'name': fields.many2one('bc.aprobaciones.departamento','Aprobaciones'),
	'users_id': fields.many2one('res.users','AM / ING / PMP'),
	'gerente_id': fields.many2one('res.users','Gerente del Área'),
	'director_id': fields.many2one('res.users','Director'),
	'bc_id': fields.many2one('business.case','Business Case'),
	}

bc_aprobaciones()

# Campos y funciones para las horas de trabajo que se mostrarán en la pestaña de Costos Operativos del BC.
class bc_horas(osv.osv):

	_name = 'bc.horas'
	_columns = {
	'bc_id': fields.many2one('business.case','Business Case'),
	#'name': fields.char('Aprobaciones', size=128),
	'horas_trabajo': fields.integer('Horas de trabajo'),
	'cadencia': fields.float('Cadencia'),
	'rol': fields.char('Rol',size=128), # cambiar....
	'pais': fields.many2one('bc.paises','País'),
	'numero_personas': fields.integer  ('Número de personas'),
	'porc_dedicacion': fields.float('% de dedicación mensual'),
	'cantidad_fte_digits': fields.float('Cantidad (FTE)',digits=(12,8)),
	'cantidad_fte': fields.float('Cantidad (FTE)'),
	'puesto_spc': fields.many2one('bc.salarios','Puesto en SPC'),
	'area_id': fields.many2one('bc.areas.especialidad', 'Sub Categoría'),
	'modo_contratacion': fields.many2one('bc.modo.contratacion','Modo de contratación'), # cambiar....
	'ubicacion': fields.many2one('bc.ubicacion.fisica','Ubicación física'), # cambiar....
	#'pago_serv_profesionales':  fields.float('Pago por servicios profesionales'),
	'salario_fte': fields.float('Salario por FTE'),
	#'bonificacion': fields.float('Bonificación por disponibilidad o zonaje'),
	#'beeper_fte': fields.char('Ubicación física',size=128), # cambiar....
	#'celular_fte': fields.char('Celular por FTE',size=128), # cambiar....
	'total': fields.float('Total'),
	'observaciones': fields.char('Observaciones',size=256),
	'salario': fields.float('Salarios'),
	'cargas_sociales': fields.float('Cargas sociales'),
	}
	def onchange_cadencia(self, cr, uid, ids, horas_trabajo, cadencia, context=None):
		model_data=self.pool.get('bc.configuracion')
		conditions = model_data.search(cr, uid, [('id', '=', 1)])
		e = model_data.read(cr, uid, conditions)
		fte=0.00
		fte=e[0]['fte']
		dedicacion_mensual=0
		if fte!=0:
			dedicacion_mensual=(float(horas_trabajo)*cadencia/fte)*100
		return {'value': {'porc_dedicacion':float(dedicacion_mensual)}}
	def onchange_horas_trabajo(self, cr, uid, ids, horas_trabajo, context=None):
		model_data=self.pool.get('bc.configuracion')
		conditions = model_data.search(cr, uid, [('id', '=', 1)])
		e = model_data.read(cr, uid, conditions)
		fte=0.00
		fte=e[0]['fte']
		cantidad_fte=0,00
		if fte!=0:
			cantidad_fte=float(horas_trabajo)/fte
		return {'value': {'cantidad_fte':float(cantidad_fte),'cantidad_fte_digits':float(cantidad_fte)}}
	def onchange_puesto_spc(self, cr, uid, ids, puesto_spc, pais, cantidad_fte_digits, cadencia, numero_personas, context=None):
		#print "PAISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS "+str(puesto_spc)
		if puesto_spc!=False:
			model_data=self.pool.get('bc.paises')
			conditions = model_data.search(cr, uid, [('id', '=', pais)])
			e = model_data.read(cr, uid, conditions)
			
			model_data=self.pool.get('bc.cargas.sociales')
			conditions = model_data.search(cr, uid, [('name', '=', pais)])
			a = model_data.read(cr, uid, conditions)
			
			
			model_data=self.pool.get('bc.salarios')
			conditions = model_data.search(cr, uid, [('id','=', puesto_spc)])
			i = model_data.read(cr, uid, conditions)
			print '\n'+str(i)+'\n\n'
			pais_a=str(e[0]['name']).replace(' ', '_').lower() #puede que falte asignar pais
			valor=float(i[0][pais_a]) #str(e[0]['name'])
			
			salario=0,00
			cargas_sociales=0,00
			if cantidad_fte_digits!=0:
				salario=float(valor)*float(cantidad_fte_digits)*float(cadencia)*float(numero_personas)
				print"valorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr: "+str(valor)
				cargas_sociales=float(float(salario)*float(a[0]['cargas'])/100)
			#print cantidad_fte
			return {'value': {'salario':float(salario), 'cargas_sociales':float(cargas_sociales)}}
		else:
			return {'value': {'salario':float(0),'cargas_sociales':float(0)}}

bc_horas()

# Campos y funciones para el total de horas de trabajo que se mostrará en la pestaña de Costos Operativos del BC.
class bc_totales_horas(osv.osv):

	_name = 'bc.totales.horas'
	_columns = {
	'bc_id': fields.many2one('business.case','Business Case'),
	#'name': fields.char('Aprobaciones', size=128),
	'area_id': fields.many2one('bc.areas.especialidad', 'Área'),
	'total_horas': fields.float('Horas'),
	'total_fte': fields.float('FTE'),
	'total_salario': fields.float('Salario'),
	'cargas_sociales': fields.float('Cargas Sociales'),
	'total_costo_horas': fields.float('Total Costo'),
	'total_venta_horas': fields.float('Total Venta'),
	}

bc_totales_horas()

# Campos y funciones para los viáticos que se mostrarán en la pestaña de Costos Operativos del BC.
class bc_viaticos(osv.osv):

	_name = 'bc.viaticos'
	_columns = {
	'bc_id': fields.many2one('business.case','Business Case'),
	#'name': fields.char('Aprobaciones', size=128),
	'pais': fields.many2one('bc.paises','País'),
	'account_id': fields.many2one('account.account', 'Cuenta de Gastos'),
	'sub_categ_id': fields.many2one('bc.viaticos.categ', 'Sub Categoría'),
	'analytic_id': fields.many2one('account.analytic.account', 'Centro de Costos'),
	#'codigo_cuenta': fields.char('Código de cuenta de gastos', size=128),
	'cantidad': fields.integer('Cantidad'),
	'costo_individual': fields.float('Costo (Individual)'),
	'total_costo': fields.float('Total costos'),
	'total_venta': fields.float('Total venta'),
	}
	
	def onchange_cantidad_costo(self, cr, uid, ids, cantidad, costo_individual, sub_categoria_id, ingreso_p, bc_id, context=None):
		#print"ipppppppppppppppppppppppppppppppppppp: "+str(ingreso_p[0][1])
		por_implementacion=0.00
		mantenimientos_ip_por=0.00
		infra_ip_por=0.00
		noc_ip_por=0.00
		result_venta=0,00
		result_costo=float(cantidad)*float(costo_individual)
		for u in ingreso_p:
			if u[2]!=False:
				model_data=self.pool.get('bc.ingreso.propuesto')
				conditions = model_data.search(cr, uid, [('id', '=', u[1])])
				e = model_data.read(cr, uid, conditions)
				#raise osv.except_osv(('Atencion!'),("\n Hubo un problema al calcular el \"Total de costos\" y el \"Total de venta\"\nIntente de nuevo con el Business Case guardado."))
				if u[2]['area_id']=="Implementación" and u[2]['porc_venta']!=False:
					por_implementacion=float(u[2]['porc_venta'])
				if u[2]['area_id']=="Mantenimiento" and u[2]['porc_venta']!=False:
					mantenimientos_ip_por=float(u[2]['porc_venta'])
				if u[2]['area_id']=="Infraestructura" and u[2]['porc_venta']!=False:
					infra_ip_por=float(u[2]['porc_venta'])
				if u[2]['area_id']=="NOC" and u[2]['porc_venta']!=False:
					noc_ip_por=float(u[2]['porc_venta'])
					
		sub = self.pool.get('bc.viaticos.categ').browse(cr, uid, sub_categoria_id, context=context)
		#print "SUBCATEG - AREA: "+str(sub.area_id.id)
		model_data=self.pool.get('bc.areas.especialidad')
		conditions = model_data.search(cr, uid, [('id', '=', sub.area_id.id)])
		e = model_data.read(cr, uid, conditions)
		#print e
		if e==[]:
			raise osv.except_osv(('Atencion!'),("\nNo se ha definido la Sub Categoría para esta línea"))
		if e[0]['name']=="Implementación": #posiblemente no se ha definido la sub categoría
				#result_venta=result_costo+(result_costo*(implementacion_ip_por*0.01))
				result_venta=result_costo+(result_costo*(por_implementacion*0.01))
		if e[0]['name']=="Mantenimiento": #posiblemente no se ha definido la sub categoría
				#result_venta=result_costo+(result_costo*(mantenimientos_ip_por*0.01))
				result_venta=result_costo+(result_costo*(mantenimientos_ip_por*0.01))
		if e[0]['name']=="Infraestructura": #posiblemente no se ha definido la sub categoría
				#result_venta=result_costo+(result_costo*(infra_ip_por*0.01))
				result_venta=result_costo+(result_costo*(infra_ip_por*0.01))
		if e[0]['name']=="NOC": #posiblemente no se ha definido la sub categoría
				#result_venta=result_costo+(result_costo*(noc_ip_por*0.01))
				result_venta=result_costo+(result_costo*(noc_ip_por*0.01))
		return {'value': {'total_costo':float(result_costo),'total_venta': float(result_venta)}}
bc_viaticos()

# Campos y funciones para los totales de viáticos que se mostrarán en la pestaña de Costos Operativos del BC.
class bc_totales_viaticos(osv.osv):

	_name = 'bc.totales.viaticos'
	_columns = {
	'bc_id': fields.many2one('business.case','Business Case'),
	'sub_categoria_id': fields.many2one('bc.areas.especialidad','Sub Categoría Case'),
	#'name': fields.char('Aprobaciones', size=128),
	#'analytic_id': fields.many2one('account.analytic.account', 'Cuenta de Gastos'),
	'total_costo_viaticos': fields.float('Costo'),
	'total_venta_viaticos': fields.float('Venta'),
	}

bc_totales_viaticos()

# Campos y funciones para los materiales adicionales que se mostrarán en la pestaña de Costos Operativos del BC.
class bc_materiles_adicionales(osv.osv):

	_name = 'bc.materiles.adicionales'
	_columns = {
	'bc_id': fields.many2one('business.case','Business Case'),
	#'name': fields.char('Aprobaciones', size=128),
	'descripcion': fields.char('Descripción', size=128),
	'cantidad': fields.integer('Cantidad'),
	'area_id': fields.many2one('bc.areas.especialidad', 'Área'),
	'costo_unitario': fields.float('Costo unitario'),
	'costo_final': fields.float('Costo final'),
	'venta_final': fields.float('Venta final'),
	}
	
	def onchange_cantidad_costo(self, cr, uid, ids, cantidad, costo_unitario, area_id, ingreso_p, context=None):
		
		por_implementacion=0.00
		mantenimientos_ip_por=0.00
		infra_ip_por=0.00
		noc_ip_por=0.00
		result_venta=0,00
		result_costo=float(cantidad)*float(costo_unitario)
				
		for u in ingreso_p:
			if u[2]!=False:
				model_data=self.pool.get('bc.ingreso.propuesto')
				conditions = model_data.search(cr, uid, [('id', '=', u[1])])
				e = model_data.read(cr, uid, conditions)
				#raise osv.except_osv(('Atencion!'),("\n Hubo un problema al calcular el \"Total de costos\" y el \"Total de venta\"\nIntente de nuevo con el Business Case guardado."))
				if u[2]['area_id']=="Implementación" and u[2]['porc_venta']!=False:
					por_implementacion=float(u[2]['porc_venta'])
				if u[2]['area_id']=="Mantenimiento" and u[2]['porc_venta']!=False:
					mantenimientos_ip_por=float(u[2]['porc_venta'])
				if u[2]['area_id']=="Infraestructura" and u[2]['porc_venta']!=False:
					infra_ip_por=float(u[2]['porc_venta'])
				if u[2]['area_id']=="NOC" and u[2]['porc_venta']!=False:
					noc_ip_por=float(u[2]['porc_venta'])
		
		
		model_data=self.pool.get('bc.areas.especialidad')
		conditions = model_data.search(cr, uid, [('id', '=', area_id)])
		e = model_data.read(cr, uid, conditions)
		if e==[]:
			raise osv.except_osv(('Atencion!'),("\nNo se ha definido la Sub Categoría para esta línea"))
		if e[0]['name']=="Implementación": #posiblemente no se ha definido la sub categoría
			#result_venta=result_costo+(result_costo*(implementacion_ip_por*0.01))
			result_venta=result_costo+(result_costo*(por_implementacion*0.01))
		if e[0]['name']=="Mantenimiento": #posiblemente no se ha definido la sub categoría
			#result_venta=result_costo+(result_costo*(mantenimientos_ip_por*0.01))
			result_venta=result_costo+(result_costo*(mantenimientos_ip_por*0.01))
		if e[0]['name']=="Infraestructura": #posiblemente no se ha definido la sub categoría
			#result_venta=result_costo+(result_costo*(infra_ip_por*0.01))
			result_venta=result_costo+(result_costo*(infra_ip_por*0.01))
		if e[0]['name']=="NOC": #posiblemente no se ha definido la sub categoría
			#result_venta=result_costo+(result_costo*(noc_ip_por*0.01))
			result_venta=result_costo+(result_costo*(noc_ip_por*0.01))
		return {'value': {'costo_final':float(result_costo),'venta_final': float(result_venta)}}

bc_materiles_adicionales()

# Campos y funciones para los totales de los materiales adicionales que se mostrarán en la pestaña de Costos Operativos del BC.
class bc_totales_adicionales(osv.osv):
	_name = 'bc.totales.adicionales'
	_columns = {
	'bc_id': fields.many2one('business.case','Business Case'),
	#'name': fields.char('Aprobaciones', size=128),
	'area_id': fields.many2one('bc.areas.especialidad', 'Área'),
	'total_costo_materiales': fields.float('Costo'),
	'total_venta_materiales': fields.float('Venta'),
	}

bc_totales_adicionales()

# Campos y funciones para el ingreso propuesto que se mostrará en la pestaña de Costos Operativos del BC.
class bc_ingreso_presupuestado(osv.osv):

	_name = 'bc.ingreso.presupuestado'
	_columns = {
	'bc_id': fields.many2one('business.case','Business Case'),
	'cdo_id': fields.many2one('bc.cdo','CDO'),
	'implementacion': fields.float('Implementación'),
	'implementacion_por': fields.float('%'),
	'mantenimientos': fields.float('Mantenimientos'),
	'mantenimientos_por': fields.float('%'),
	'infraestructura': fields.float('Infraestructura'),
	'infraestructura_por': fields.float('%'),
	'noc': fields.float('NOC'),
	'noc_por': fields.float('%'),

	}

bc_ingreso_presupuestado()

# Campos y funciones para el ingreso de productos que se mostrará en la pestaña del BOM Equipo.

class bc_bom_equipo(osv.osv):

	_name = 'bc.bom.equipo'




	'''_columns = {
				'partner_id': fields.related('order_id','partner_id',string='Partner',type="many2one", relation="res.partner", store=True),
				'otro_proveedor_id': fields.many2one('res.partner','Nombre del Proveedor (en caso de ser otro)'),
				'available':fields.function(_count_available,string='Disponibles',type='float',method=True,store=True, required=False),
				'precio_lista': fields.float('Precio lista'),
				'descuento': fields.float('Descuento'),
				'precio_costo': fields.float('Precio Costo'),
				'precio_venta': fields.float('Precio Venta'),
				'utilidad': fields.float('Utilidad'),
				'margen': fields.float('Margen'),#function(_count_marg,type='float',method=True,store=True),
				'price_subtotal': fields.function(_amount_line, string='Subtotal11', digits_compute= dp.get_precision('Account')),
				'cost_sin_imp':fields.float('Precio sin Impuestos'),
				'tax_id_mio':fields.float('Impuesto de Venta'),
	}'''
	def _get_cargar(self, cr, uid, ids, name, args, context=None):
		this = self.browse(cr, uid, ids, context=context)[0]
		res={}
		id=0
		for line in self.browse(cr, uid, ids, context=context):
			id=line.id
		res[id]=False
		return res

	def _amount_all(self, cr, uid, ids, name, args, context=None):

		
		preciol_unitario=0.00
		descuento=0.00
		precio_cu=0.00
		cantidad=0.00
		porc_utilidad=0.00
		porc_iva=0.00
		precio_tu=0.00
		res = {}

		#print '\n\nname '+str(name)+'\n\nargs '+str(args)+'\n\n'+'\n\ncontext '+str(context)+'\n\n'
		id=0
		for line in self.browse(cr, uid, ids, context=context):

			preciol_unitario=line.preciol_unitario
			descuento=line.descuento
			precio_cu=line.precio_cu
			cantidad=line.cantidad
			porc_utilidad=line.porc_utilidad
			porc_iva= 1 #line.porc_iva
			id=line.id
			#print "IMPUESTOSSSSSSSS: "+str(line.tax_id[0].name)
			impuestos=line.tax_id

		precio_cu=(preciol_unitario-float(preciol_unitario*(descuento*0.01)))
		total_costo=precio_cu*cantidad
		solita=(1-(porc_utilidad*0.01))
		precio_unitario=(precio_cu/solita)
		precio_total=precio_unitario*cantidad
		#print "IMP: "+str(impuestos)
		if impuestos!=[]:
			for i in impuestos:
				precio_tu=float(precio_tu)+float(precio_unitario)+(float(precio_unitario)*(float(i.amount)))
		else:
			precio_tu=precio_unitario
		precio_total_ivi=precio_tu*cantidad
		if name == 'precio_cu':res[id] = precio_cu
		if name == 'total_costo':res[id] = total_costo
		if name == 'precio_unitario':res[id] = precio_unitario
		if name == 'precio_total':res[id] = precio_total
		if name == 'precio_tu':res[id] = precio_tu
		if name == 'precio_total_ivi':res[id] = precio_total_ivi
		#print "FUNCIONAL: "+str(res)
		return res
	
	_columns = {
	'bc_id': fields.many2one('business.case','Business Case'),
	#'name': fields.char('Aprobaciones', size=128),
	#'analytic_id': fields.many2one('account.analytic.account', 'Centro Costo'),
	'otro_proveedor_id': fields.many2one('res.partner','Nombre del Proveedor (en caso de ser otro)'),
	'bom_tipo': fields.selection([('product','product'),('service','service'),('consu','consu')], 'Tipo', help="Tipo de producto en el sistema(Necesario para Cargar productos)"),
	'proveedor_id': fields.many2one('res.partner','Proveedor',required=True),
	'codigo_producto':fields.char('Codigo',size=64 ),
	'product_id':fields.many2one('product.product', 'Producto', domain=[('sale_ok', '=', True)], change_default=True),
	'descripcion_producto': fields.char('Descripción', size=128),
	'preciol_unitario':fields.float('Precio lista unitario'),
	'descuento': fields.float('Descuento'),
	'precio_cu': fields.function(_amount_all, method=True, type="float",string='Precio costo unitario',digits_compute=dp.get_precision('Account'),store=True),
	'cantidad': fields.integer('Cantidad'),
	'total_costo': fields.function(_amount_all, method=True, type="float",string='Total costo',digits_compute=dp.get_precision('Account'),store=True),
	'porc_utilidad': fields.float('% Utilidad'),
	'precio_unitario': fields.function(_amount_all, method=True, type="float",string='Precio unitario',digits_compute=dp.get_precision('Account'),store=True),
	'precio_total': fields.function(_amount_all, method=True, type="float",string='Precio total',digits_compute=dp.get_precision('Account'),store=True),
	
	'tax_id': fields.many2many('account.tax', 'business_bom_order_tax', 'bom_line_id', 'tax_id', 'Impuestos', readonly=True, states={'draft': [('readonly', False)]}),
	
	'imp_ventas_unitario': fields.float('Impuesto de Ventas Unitario'),
	'imp_ventas_total': fields.float('Impuesto de Ventas Total (Linea)'),
	'precio_tu': fields.function(_amount_all, method=True, type="float",string='Precio total unitario (IVI)',digits_compute=dp.get_precision('Account'),store=True),
	'precio_total_ivi': fields.function(_amount_all, method=True, type="float",string='Precio total (línea IVI)',digits_compute=dp.get_precision('Account'),store=True),
	'cargar': fields.boolean('Cargar'),
	'stadito' : fields.char('estadito',size=64),
	'categoria_id': fields.many2one('bc.bom.categorias','Categoria'),
	'observaciones' : fields.text('Observaciones'),
	'rel_proyecto': fields.many2one('project.project','Proyecto'),
	}
	_defaults = {
			'cargar': False,
			'stadito': 'draft'
		}

	def change_cod(self, cr, uid, ids,cod_prod,context=None):

		#print '\n\naaa '+str(ids)+'\n\nbbb '+str(cod_prod)+'\n\n'+str(context)+'\n\n'+str(context)+'\n\n'
		values= \
			{'value':
				 {
				 'descripcion_producto':cod_prod,
				 }
			}
		return values




	def create_products(self, cr, uid,  ids,cargar,descripcion_producto,codigo_producto,tipo,categoria_id, context=None):
		#print '\n\n\n\nprimero55 '+str(categoria_id)
		var=0
		if cargar==True:
			#print '\n\n\n\nprimero55'
			if tipo not in ['product','service','consu']:
				raise osv.except_osv(('Atencion!'),("\n Elija un tipo de producto correcto"))

			var= self.pool.get('product.product').create(cr,uid,{'name':descripcion_producto,'default_code':codigo_producto,'type':tipo,'type_bom':categoria_id,'company_id':False},context=None)
			#print '\n\n\n\nproducto'+str( var)
			#return var
			# Notice how we don't pass id_classb value here,
			# it is implicit when we write one2many field
		'''record.write({'bom_equipo_id': sub_lines}, context=context)'''
		#self.write(cr,uid,ids,{'name':'TIERRA'},context=context)
		return {'value':{'product_id':var}}



	def product_id_change(self, cr, uid, ids,product, context=None):
		res =res = self.pool.get('product.product').browse(cr, uid, product, context=context)
		if product!=False: return {'value':{'codigo_producto' :res.code,'descripcion_producto' :res.name}}
		else: return {'value':{'codigo_producto' :'','descripcion_producto' :''}}

	def get_codigo(self, cr, uid, ids,letras, context=None):
		res = self.pool.get('product.product').name_search(cr, uid, letras, args=None, operator='ilike', context=None, limit=100)
		#print '\n\n'+str(res)+'\n\n'
		return {'value':{'descripcion_producto' :'aaaa'}}


	def calculo(self, cr, uid, ids,preciol_unitario,descuento,precio_cu,cantidad,porc_utilidad,context=None):
		precio_cu=(preciol_unitario-float(preciol_unitario*(descuento*0.01)))
		porc_iva=0
		precio_tu=0
		total_costo=precio_cu*cantidad
		solita=(1-(porc_utilidad*0.01))
		precio_unitario=(precio_cu/solita)
		precio_total=precio_unitario*cantidad
		if porc_iva!=0:
			precio_tu=precio_unitario+(precio_unitario*(porc_iva*0.01))
		precio_total_ivi=precio_tu*cantidad
		values= \
			{'value':
					 {
						 'precio_cu':precio_cu,
						 'total_costo':total_costo,
						 'precio_unitario':precio_unitario,
						 'precio_total':precio_total,
						 'precio_tu':precio_tu,
						 'precio_total_ivi':precio_total_ivi
					 }
			}
		return values



	'''def create(self, cr, uid, vals, context=None):


		preciol_unitario=vals.get('preciol_unitario',0)
		descuento=vals.get('descuento',0)
		precio_cu=vals.get('precio_cu',0)
		cantidad=vals.get('cantidad',0)
		porc_utilidad=vals.get('porc_utilidad',0)
		porc_iva=vals.get('porc_iva',0)

		precio_cu=(preciol_unitario-float(preciol_unitario*(descuento*0.01)))
		total_costo=precio_cu*cantidad
		solita=(1-(porc_utilidad*0.01))
		precio_unitario=(precio_cu/solita)
		precio_total=precio_unitario*cantidad
		precio_tu=precio_unitario+(precio_unitario*(porc_iva*0.01))
		precio_total_ivi=precio_tu*cantidad
		vals.update({'precio_cu':precio_cu})
		vals.update({'total_costo':total_costo})
		vals.update({'precio_unitario':precio_unitario})
		vals.update({'precio_total':precio_total})
		#vals.update({'precio_tu':precio_tu})
		vals.update({'precio_total_ivi':precio_total_ivi})

		fila = super(bc_bom_equipo, self).create(cr, uid, vals, context=context)

		return fila'''


	'''def write(self, cr, uid, ids, vals, context=None):

		preciol_unitario=0
		descuento=0
		precio_cu=0
		cantidad=0
		porc_utilidad=0
		porc_iva=0
		#print '\n\nvalores '+str(vals)+'\n\n'+str(context)+'\n\n'+str(ids)+'\n\n'
		for line in self.browse(cr, uid, ids):

			if vals.get('preciol_unitario','')=='':
				preciol_unitario=line.preciol_unitario

			if vals.get('descuento','')=='':
				descuento=line.descuento

			if vals.get('precio_cu','')=='':
				precio_cu=line.precio_cu
			if vals.get('cantidad','')=='':
				cantidad=line.cantidad

			if vals.get('porc_utilidad','')=='':
				porc_utilidad=line.porc_utilidad


		precio_cu=(preciol_unitario-float(preciol_unitario*(descuento*0.01)))
		total_costo=precio_cu*cantidad
		solita=(1-(porc_utilidad*0.01))
		precio_unitario=(precio_cu/solita)
		precio_total=precio_unitario*cantidad
		precio_tu=precio_unitario+(precio_unitario*(porc_iva*0.01))
		precio_total_ivi=precio_tu*cantidad

		vals.update({'precio_cu':precio_cu})
		vals.update({'total_costo':total_costo})
		vals.update({'precio_unitario':precio_unitario})
		vals.update({'precio_total':precio_total})
		#vals.update({'precio_tu':precio_tu})
		vals.update({'precio_total_ivi':precio_total_ivi})
		#print '\n\n'+str(vals)+'\n\n'
		x = super(bc_bom_equipo,self).write(cr, uid, ids, vals, context=context)
		return x'''

bc_bom_equipo()


# Campos y funciones para el margen de operación del BC.
class bc_margen_operacion(osv.osv):

	_name = 'bc.margen.operacion'
	_columns = {
	'bc_id': fields.many2one('business.case','Business Case'),
	'name': fields.many2one('bc.cdo.margen','CDO'),
	
	'monto_implementacion':fields.float('Implementación'),
	
	#'porc_implementacion': fields.float('%'),
	
	'monto_mantenimientos': fields.float('Mantenimientos'),
	#'porc_mantenimientos': fields.float('%'),
	
	'monto_noc': fields.float('NOC'),
	#'porc_noc': fields.float('%'),
	

	'monto_infraestructura': fields.float('Infraestructura'),
	#'porc_infraestructura': fields.float('%'),

	'monto_equipos': fields.float('Equipos'),
	#'porc_equipos': fields.float('%'),

	'monto_total': fields.float('TOTAL'),
	#'porc_total': fields.float('%'),
	
	}

bc_margen_operacion()


class bc_montos_indicadores(osv.osv):

	_name = 'bc.montos.indicadores'
	_columns = {
	'bc_id': fields.many2one('business.case','Business Case'),
	'name': fields.many2one('bc.indicadores','Indicadores'),
	'indicador_implementacion': fields.float('Implementacion'),
	'indicador_mantenimientos': fields.float('Mantenimientos'),
	'indicador_noc': fields.float('NOC'),
	'indicador_infraestructura': fields.float('Infraestructura'),
	'indicador_equipos': fields.float('Equipos'),
	'indicador_total': fields.float('Total'),
	
	}

bc_montos_indicadores()

class bc_areas_especialidad(osv.osv):
	_name = 'bc.areas.especialidad'
	_columns = {
		'name': fields.char('Nombre', size=128),
	}
bc_areas_especialidad()

class bc_viaticos_categ(osv.osv):
	_name = 'bc.viaticos.categ'
	_columns = {
		'name': fields.char('Nombre', size=128),
		'area_id': fields.many2one('bc.areas.especialidad','Área',required=True),
	}
bc_viaticos_categ()

class bc_cf(osv.osv):
	_name = 'bc.cf'
	_columns = {
		'name': fields.char('Nombre', size=128),
	}
bc_cf()

class bc_cargas_sociales(osv.osv):
	_name = 'bc.cargas.sociales'
	_columns = {
		'name': fields.many2one('bc.paises','Pais'),
		'ubicacion': fields.integer('Ubicacion'),
		'cargas': fields.float('Cargas Sociales'),
	}
bc_cargas_sociales()

class bc_salarios(osv.osv):
	_name = 'bc.salarios'
	_columns = {
		'name': fields.char('Perfiles Técnicos', size=128),
		'costa_rica': fields.float('Costa Rica'),
		'guatemala': fields.float('Guatemala'),
		'el_salvador': fields.float('El Salvador'),
		'nicaragua': fields.float('Nicaragua'),
		'honduras': fields.float('Honduras'),
	}
bc_salarios()

class bc_configuracion(osv.osv):
	_name = 'bc.configuracion'
	_columns = {
		'fte': fields.float('FTE'),
	}
	def default_get(self, cr, uid, fields, context=None):
		res = super(bc_configuracion, self).default_get(cr, uid, fields, context=context)
		model_data=self.pool.get('bc.configuracion')
		conditions = model_data.search(cr, uid, [('id', '=', 1)])
		print conditions
		if conditions!=[]:
			e = model_data.read(cr, uid, conditions)
			res['fte']=e[0]['fte']
			return res
		else:
			return True
	
	def apply_conf(self, cr, uid, ids, context=None):
		self.pool.get('bc.configuracion').write(cr, uid, 1, {'fte': float(context['fte']),},context=context)
		model_data=self.pool.get('bc.configuracion')
		list_ids = model_data.search(cr, uid, [])
		list_ids.remove(1)
		self.pool.get('bc.configuracion').unlink(cr, uid, list_ids, context=None)
		return True
	
	def create(self, cr, uid, vals, context=None):
		fila = super(bc_configuracion, self).create(cr, uid, vals, context=context)
		return fila
	
bc_configuracion()

class bc_paises(osv.osv):
	_name = 'bc.paises'
	_columns = {
		'name': fields.char('País', size=128),
	}
bc_paises()

class bc_aprobaciones_departamento(osv.osv):
	_name = 'bc.aprobaciones.departamento'
	_columns = {
		'name': fields.char('Aprobación', size=128),
	}
bc_aprobaciones_departamento()

class bc_cdo(osv.osv):
	_name = 'bc.cdo'
	_columns = {
		'name': fields.char('Indicador', size=128),
	}
bc_cdo()

class bc_cdo_margen(osv.osv):
	_name = 'bc.cdo.margen'
	_columns = {
		'name': fields.char('CDO', size=128),
	}
bc_cdo_margen()

class bc_indicadores(osv.osv):
	_name = 'bc.indicadores'
	_columns = {
		'name': fields.char('Indicadores', size=128),
	}
bc_indicadores()

class bc_ingreso_propuesto(osv.osv):
	_name = 'bc.ingreso.propuesto'
	_columns = {
		'bc_id': fields.many2one('business.case','Business Case'),
		'area_id': fields.many2one('bc.areas.especialidad','Área',readonly=True),
		'monto_venta': fields.float('Venta',readonly=True),
		'porc_venta': fields.float('Porcentaje'),
	}
	#Metodo para aplicar cambios en los montos al cambiar los porcentaje de ingreso propuesto
	def onchange_porc_venta(self, cr, uid, ids, horas_totales, totales_viaticos, totales_adicionales, costo_operacion, margen_contribucion, viaticos ,adicionales, area_id, monto_venta_p, porcentaje, context=None):
		print"\n\nPorcentaje de venta\n\n"
		print"Area: "+str(area_id)
		print"Adicionales: "+str(adicionales)
		#CAMBIA LOS MONTOS DE LOS MATERIALES ADICIONALES DESDE INGRRESO PROPUESTO
		pool_via=self.pool.get('bc.viaticos')
		for v in viaticos:
			via=pool_via.browse(cr, uid, v[1], context=context)
			if via.sub_categ_id.area_id.id==area_id:
				total_venta=via.total_costo+(via.total_costo*(porcentaje*0.01))
				pool_via.write(cr, uid, via.id, {'total_venta': total_venta},context=context)
				print"ESCRITURA REALIZADA EN: "+str(v[1])+"- "+str(via.sub_categ_id.name)
		#CAMBIA LOS MONTOS DE LOS MATERIALES ADICIONALES DESDE INGRRESO PROPUESTO
		pool_adi=self.pool.get('bc.materiles.adicionales')
		for a in adicionales:
			adi=pool_adi.browse(cr, uid, a[1], context=context)
			if adi.area_id.id==area_id:
				venta_final=adi.costo_final+(adi.costo_final*(porcentaje*0.01))
				pool_adi.write(cr, uid, adi.id, {'venta_final': venta_final},context=context)
				print"ESCRITURA REALIZADA EN: "+str(a[1])+"- "+str(adi.descripcion)
		#CAMBIA EL TOTAL DE LAS HORAS DE TRABAJO SEGUN EL PORCENTAJE EN INGRESO PROPUESTO
		pool_hto=self.pool.get('bc.totales.horas')
		for h in horas_totales:
			hto=pool_hto.browse(cr, uid, h[1], context=context)
			if hto.area_id.id==area_id:
				total_venta_horas=hto.total_costo_horas+(hto.total_costo_horas*(porcentaje*0.01))
				pool_hto.write(cr, uid, hto.id, {'total_venta_horas': total_venta_horas},context=context)
				print"ESCRITURA REALIZADA EN: "+str(h[1])+"- "+str(hto.area_id.name)
		#CAMBIA EL TOTAL DE VIATICOS SEGUN EL PORCENTAJE EN INGRESO PROPUESTO
		pool_tvi=self.pool.get('bc.totales.viaticos')
		for tv in totales_viaticos:
			tvi=pool_tvi.browse(cr, uid, tv[1], context=context)
			if tvi.sub_categoria_id.id==area_id:
				total_venta_viaticos=tvi.total_costo_viaticos+(tvi.total_costo_viaticos*(porcentaje*0.01))
				pool_tvi.write(cr, uid, tvi.id, {'total_venta_viaticos': total_venta_viaticos},context=context)
				print"ESCRITURA REALIZADA EN: "+str(tv[1])+"- "+str(tvi.sub_categoria_id.name)
		#CAMBIA EL TOTAL DE MATERIALES ADICIONALES SEGUN EL PORCENTAJE EN INGRESO PROPUESTO
		pool_tad=self.pool.get('bc.totales.adicionales')
		for ta in totales_adicionales:
			tad=pool_tad.browse(cr, uid, ta[1], context=context)
			if tad.area_id.id==area_id:
				total_venta_materiales=tad.total_costo_materiales+(tad.total_costo_materiales*(porcentaje*0.01))
				pool_tad.write(cr, uid, tad.id, {'total_venta_materiales': total_venta_materiales},context=context)
				print"ESCRITURA REALIZADA EN: "+str(ta[1])+"- "+str(tad.area_id.name)
		#CAMBIA EL TOTAL DE VENTA DE INGRESO PROPUESTO(SELF)
		pool_cop=self.pool.get('bc.costo.operacion')
		for co in costo_operacion:
			cop=pool_cop.browse(cr, uid, co[1], context=context)
			if cop.area_id.id==area_id:
				monto_venta=cop.monto_costo/(1-(float(porcentaje)*0.01))
				self.write(cr, uid, cop.id, {'monto_venta': monto_venta},context=context)
				print"ESCRITURA REALIZADA EN: "+str(co[1])+"- "+str(cop.area_id.name)
		#CAMBIA EL MARGEN DE CONTRIBUCION SEGUN EL PORCENTAJE DE VENTA DE INGRESO PROPUESTO
		
		
		pool_contr=self.pool.get('bc.margen.contribucion')
		for mc in margen_contribucion:
			contr=pool_contr.browse(cr, uid, mc[1], context=context)
			print contr.area_id.name
			if contr.area_id.id==area_id:
				monto_contribucion=monto_venta_p*float(contr.porc_contribucion*0.01)
				print monto_contribucion
				pool_contr.write(cr, uid, contr.id, {'monto_contribucion': monto_contribucion},context=context)
				print"ESCRITURA REALIZADA EN MARGEN DE CONTRIBUCION: "+str(mc[1])+"- "+str(contr.area_id.name)
		
		
		return True
bc_ingreso_propuesto()

class bc_costo_operacion(osv.osv):
	_name = 'bc.costo.operacion'
	_columns = {
		'bc_id': fields.many2one('business.case','Business Case'),
		'area_id': fields.many2one('bc.areas.especialidad','Área', readonly=True),
		'monto_costo': fields.float('Costo', readonly=True),
	}
bc_costo_operacion()

class bc_margen_contribucion(osv.osv):
	_name = 'bc.margen.contribucion'
	_columns = {
		'bc_id': fields.many2one('business.case','Business Case'),
		'area_id': fields.many2one('bc.areas.especialidad','Área', readonly=True),
		'monto_contribucion': fields.float('Monto',readonly=True),
		'porc_contribucion': fields.float('Porcentaje'),
	}
bc_margen_contribucion()

class res_partner(osv.osv):
	_inherit = 'res.partner'
	_columns = {
		'parent_id_bc': fields.many2one('business.case','business Case'),
	}
res_partner()

class bc_bom_categorias(osv.osv):
	_name = 'bc.bom.categorias'
	_columns = {
		'name': fields.char('Categoría', size=128),
	}
bc_bom_categorias()

class bc_modo_contratacion(osv.osv):
	_name = 'bc.modo.contratacion'
	_columns = {
		'name': fields.char('Modo de contratación', size=128),
	}
bc_modo_contratacion()

class bc_ubicacion_fisica(osv.osv):
	_name = 'bc.ubicacion.fisica'
	_columns = {
		'name': fields.char('Ubicación física', size=128),
	}
bc_ubicacion_fisica()

class product_product(osv.osv):
	_name = 'product.product'
	_inherit = 'product.product'
	_columns={
		'type_bom': fields.many2one('bc.bom.categorias', 'Tipo Bom', help="Categoría utilizada en el Business Case y en Proyectos"),
	}
product_product()

#SUBIR A RAMA
class enviar_mensajes(osv.osv_memory):
    _name = 'enviar.mensajes'
    _inherit = ['mail.compose.message']

    _columns = {
	    'name': fields.char('Nombre'),
	    'mi_campo':fields.char("Manage different units of measure for products",
			help="""Allows you to select and maintain different units of measure for products.""", size=64),
	    'prueba': fields.boolean('Campito'),

	    'composition_mode': fields.selection(
		    lambda s, *a, **k: s._get_composition_mode_selection(*a, **k),
		    string='Composition mode'),
	    'partner_ids': fields.many2many('res.partner',
	                                    'mail_compose_message_businesscase_rel',
	                                    'wizard_id', 'partner_id', 'Additional contacts'),
	    'attachment_ids': fields.many2many('ir.attachment',
	                                       'mail_compose_message_ir_attachments_businesscase_rel',
	                                       'wizard_id', 'attachment_id', 'Attachments'),
	    'filter_id': fields.many2one('ir.filters', 'Filters'),
        }

    def send_mail_businesscase(self, cr, uid, ids, context=None):
        print "\n\n\nEstoy aqui :-docxedxcsd\n\n\n"

        if context is None:
            context = {}
        ir_attachment_obj = self.pool.get('ir.attachment')
        active_ids = context.get('active_ids')
        is_log = context.get('mail_compose_log', False)
	aa=False
        for wizard in self.browse(cr, uid, ids, context=context):
            mass_mail_mode = wizard.composition_mode == 'mass_mail'
            active_model_pool_name = wizard.model if wizard.model else 'mail.thread'
            active_model_pool = self.pool.get(active_model_pool_name)
	    aa=wizard
            # wizard works in batch mode: [res_id] or active_ids
            res_ids = active_ids if mass_mail_mode and wizard.model and active_ids else [wizard.res_id]
            for res_id in res_ids:
		print "\n\n wizard.subject: " + str(wizard.parent_id)
		print "\n\n wizard.partner_ids: " + str(wizard.partner_ids)
                # mail.message values, according to the wizard options
                post_values = {
                    'subject': wizard.subject,
                    'body': wizard.body,
                    'parent_id': wizard.parent_id and wizard.parent_id.id,
                    'partner_ids': [partner.id for partner in wizard.partner_ids],
                    'attachment_ids': [attach.id for attach in wizard.attachment_ids],
                }
		#print '\n\npost_values '+str(post_values['parent_id']._name)+'\n\n'
                # mass mailing: render and override default values
                if mass_mail_mode and wizard.model:
                    email_dict = self.render_message(cr, uid, wizard, res_id, context=context)
                    post_values['partner_ids'] += email_dict.pop('partner_ids', [])
                    print '\n\nemail_dict '+str(email_dict)+'\n\n'
                    post_values['attachments'] = email_dict.pop('attachments', [])
                    attachment_ids = []
                    for attach_id in post_values.pop('attachment_ids'):
                        new_attach_id = ir_attachment_obj.copy(cr, uid, attach_id, {'res_model': self._name, 'res_id': wizard.id}, context=context)
                        attachment_ids.append(new_attach_id)
                    post_values['attachment_ids'] = attachment_ids
                    post_values.update(email_dict)
                # post the message
                subtype = 'mail.mt_comment'
                if is_log:  # log a note: subtype is False
                    subtype = False
                elif mass_mail_mode:  # mass mail: is a log pushed to recipients, author not added
                    subtype = False
                    context = dict(context, mail_create_nosubscribe=True)  # add context key to avoid subscribing the author
                msg_id = active_model_pool.message_post(cr, uid, [res_id], type='comment', subtype=subtype, context=context, **post_values)
                # mass_mailing: notify specific partners, because subtype was False, and no-one was notified
                if mass_mail_mode and post_values['partner_ids']:
                    self.pool.get('mail.notification')._notify(cr, uid, msg_id, post_values['partner_ids'], context=context)
	# Antes cambia de estado el Proyecto.
	print '\n\nwizardddd '+str(aa)+'\n\n'+str(context)+'\n\n'+str(aa._columns)+'\n\n'

	#project = self.pool.get('project.project').write(cr,uid,context.get('active_id','active_ids'),{'state': 'pending'})

        return {'type': 'ir.actions.act_window_close'}

# Productos para las areas.
class areas_productos(osv.osv):
    _name = 'bc.areas.productos'

    _columns = {
	    'name': fields.char('Nombre del Área', required=True),
	    'product_id': fields.many2one('product.product', 'Producto', required=True)
    }

areas_productos()

