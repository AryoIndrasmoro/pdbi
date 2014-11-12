# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields,osv
import openerp.addons.decimal_precision as dp
#from openerp.tools.translate import _

class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {        
        'type_id'         :fields.many2one('customer.type', 'Type'),
        'industry_id'     :fields.many2one('customer.industry', 'Industry'),
        'last_name'       :fields.char('Last Name'),        
    }        

res_partner()

class customer_type(osv.osv):
    _name = 'customer.type'
    _columns = {
        'name'              : fields.char('Type'),                    
        'description'       : fields.char('Description'),
    }
    
customer_type()

class customer_industry(osv.osv):
    _name = 'customer.industry'
    _columns = {
        'name'              : fields.char('Industry'),                    
        'description'       : fields.char('Description'),
    }
    
customer_industry()

class event_pdbi(osv.osv):
    _name = 'event.pdbi'
    _columns = {
        'name'              : fields.char('Event Name'),                    
        'date'              : fields.date('Date'),
        'customer_ids'      : fields.many2many('res.partner','res_partner_event_pdbi_rel','eid','pid','Customers', domain=[('customer','=', True)]),
    }
    
event_pdbi()