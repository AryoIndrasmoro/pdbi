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
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
#from openerp.tools.translate import _

class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {        
        'type_id'         :fields.many2one('customer.type', 'Type'),
        'industry_id'     :fields.many2one('customer.industry', 'Industry'),
        'last_name'       :fields.char('Last Name'),
        'created_by'      :fields.many2one('res.users', 'Created By'),
        'created_date'    :fields.char('Created Date'),
    }        
    
    _defaults = {
                 'created_by' : lambda obj, cr, uid, context: uid,
                 'created_date': lambda *a: time.strftime('%Y-%m-01'),
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
        'partner_ids'       : fields.many2many('res.partner', 'name', id2='partner_id', string='Customers'),            
    }
    
    def create_event(self, cr, uid, ids, context=None):
        state_name = ''        
        state_id  = self.pool.get('customer.state').search(cr, uid, [('name','=','Not Started')], context=None)
        if state_id:
            state_obj = self.pool.get('customer.state').browse(cr, uid, state_id, context=None)                    
            for state in state_obj:
                print state.name
                state_name = state.id
                                        
        for event in self.browse(cr, uid, ids, context=context):            
            for partner in event.partner_ids:                
                self.pool.get('customer.event').create(cr, uid, {
                        'event_id': event.id,
                        'customer_id': partner.id,
                        'created_by':uid,
                        'state':state_name,
                        'event_date':event.date
                    })        
        return True
    
event_pdbi()

class customer_event(osv.osv):
    _name = 'customer.event'
    _columns = {
        'event_id'          : fields.many2one('event.pdbi','Event Name'),
        'event_date'        : fields.date('Event Date'),
        'created_by'        : fields.many2one('res.users','Created By'),                    
        'customer_id'       : fields.many2one('res.partner','Customer', domain=[('customer','=',True)]),
        'state'             : fields.many2one('customer.state','State'),
        'notes'             : fields.text('Notes'),                                    
    }
    
    def create(self, cr, uid, vals, context=None):
        new_id = super(customer_event, self).create(cr, uid, vals, context=context)        
        return new_id    
    
customer_event()

class customer_state(osv.osv):
    _name = 'customer.state'
    _columns = {
        'name'          : fields.char('Status'),
        'description'   : fields.char('Description'),                                        
    }        
    
customer_state()