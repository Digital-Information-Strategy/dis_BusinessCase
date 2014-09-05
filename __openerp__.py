# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 DIS S.A. (<http://www.dis.co.cr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name" : "Business Case",
    "version" : "1.0",
    "author" : "DIS S.A.",
    "category" : "Tools",
    "website" : "http://www.dis.co.cr",
    "description": """ Este módulo permite almacenar en el sistema los casos de negocio para cada proyecto junto con sus respectivos cálculos operativos. Dicho caso de negocio permitirá alojar el detalle total de cada venta realizada y cada venta por realizar en la empresa.
    """,
    'depends': ['base','mail','base_setup','account','crm','sale','project','purchase','product','hr'],
    "update_xml" : [ ],
    'init_xml':['data/data.xml'],
    'data': ['views/BusinessCase_view.xml','security/bc_security.xml','security/ir.model.access.csv',],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
