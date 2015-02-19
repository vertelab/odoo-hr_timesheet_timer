# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
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

from datetime import datetime, timedelta
import itertools
from lxml import etree
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

import logging

_logger = logging.getLogger(__name__)

class account_analytic_line(models.Model):
    _inherit = "account.analytic.line"
    
    start_time  = fields.Datetime(string="Start time", default=fields.Datetime.now)
    stop_time   = fields.Datetime(string="Stop time")

class hr_analytic_timesheet(models.Model):
    _inherit = "hr.analytic.timesheet"
    
    @api.onchange('start_time', 'stop_time')
    def onchange_timesheet_timer_start_stop_time(self):
        if self.start_time and self.stop_time:
            self.unit_amount = (datetime.strptime(self.stop_time, 
            '%Y-%m-%d %H:%M:%S') - datetime.strptime(self.start_time, 
            '%Y-%m-%d %H:%M:%S')).seconds / 3600.0

class project_work(models.Model):
    _inherit = "project.task.work"
    
    start_time  = fields.Datetime(string="Start time", default=fields.Datetime.now)
    stop_time   = fields.Datetime(string="Stop time")
    
    def _create_analytic_entries(self, cr, uid, vals, context):
        timeline_id = super(project_work, self)._create_analytic_entries(cr, uid, vals, context)
        if timeline_id:
            timesheet = self.pool.get('hr.analytic.timesheet').browse(cr,uid,timeline_id,context)[0]
            updv = { 'start_time': self.start_time, 'stop_time': self.stop_time }
            timesheet.write(cr, uid, [timeline_id], updv, context=context)
        return timeline_id
        
    def write(self, cr, uid, ids, vals, context=None):
        """
        When a project task work gets updated, handle its hr analytic timesheet.
        """
        if context is None:
            context = {}
        timesheet_obj = self.pool.get('hr.analytic.timesheet')
        uom_obj = self.pool.get('product.uom')
        result = {}

        if isinstance(ids, (long, int)):
            ids = [ids]

        for task in self.browse(cr, uid, ids, context=context):
            line_id = task.hr_analytic_timesheet_id
            if not line_id:
                # if a record is deleted from timesheet, the line_id will become
                # null because of the foreign key on-delete=set null
                continue

            vals_line = {}
            if 'name' in vals:
                vals_line['name'] = '%s: %s' % (tools.ustr(task.task_id.name), tools.ustr(vals['name'] or '/'))
            if 'user_id' in vals:
                vals_line['user_id'] = vals['user_id']
            if 'date' in vals:
                vals_line['date'] = vals['date'][:10]
            if 'start_time' in vals:
                vals_line['start_time'] = vals['start_time']
            if 'stop_time' in vals:
                vals_line['stop_time'] = vals['stop_time']
            if 'hours' in vals:
                vals_line['unit_amount'] = vals['hours']
                prod_id = vals_line.get('product_id', line_id.product_id.id) # False may be set

                # Put user related details in analytic timesheet values
                details = self.get_user_related_details(cr, uid, vals.get('user_id', task.user_id.id))
                for field in ('product_id', 'general_account_id', 'journal_id', 'product_uom_id'):
                    if details.get(field, False):
                        vals_line[field] = details[field]

                # Check if user's default UOM differs from product's UOM
                user_default_uom_id = self.pool.get('res.users').browse(cr, uid, uid).company_id.project_time_mode_id.id
                if details.get('product_uom_id', False) and details['product_uom_id'] != user_default_uom_id:
                    vals_line['unit_amount'] = uom_obj._compute_qty(cr, uid, user_default_uom_id, vals['hours'], details['product_uom_id'])

                # Compute based on pricetype
                amount_unit = timesheet_obj.on_change_unit_amount(cr, uid, line_id.id,
                    prod_id=prod_id, company_id=False,
                    unit_amount=vals_line['unit_amount'], unit=False, journal_id=vals_line['journal_id'], context=context)

                if amount_unit and 'amount' in amount_unit.get('value',{}):
                    vals_line['amount'] = amount_unit['value']['amount']

            if vals_line:
                self.pool.get('hr.analytic.timesheet').write(cr, uid, [line_id.id], vals_line, context=context)

        return super(project_work,self).write(cr, uid, ids, vals, context)

    @api.onchange('start_time', 'stop_time')
    def onchange_timesheet_timer_start_stop_time(self):
        if self.start_time and self.stop_time:
            self.hours = (datetime.strptime(self.stop_time, 
            '%Y-%m-%d %H:%M:%S') - datetime.strptime(self.start_time, 
            '%Y-%m-%d %H:%M:%S')).seconds / 3600.0

"""
class project_work_task(models.Model):
    _inherit = "project.task"
    
    @api.onchange('start_time', 'stop_time')
    def onchange_timesheet_timer_start_stop_time(self):
        if self.start_time and self.stop_time:
            self.hours = (datetime.strptime(self.stop_time, 
            '%Y-%m-%d %H:%M:%S') - datetime.strptime(self.start_time, 
            '%Y-%m-%d %H:%M:%S')).seconds / 3600.0
"""
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
