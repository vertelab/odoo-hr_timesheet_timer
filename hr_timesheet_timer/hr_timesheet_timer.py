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
from openerp import models, fields, api, _, tools
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
            tools.DEFAULT_SERVER_DATETIME_FORMAT) - datetime.strptime(self.start_time, 
            tools.DEFAULT_SERVER_DATETIME_FORMAT)).seconds / 3600.0
"""
class project_work(osv.osv):
    _inherit = "project.task.work"
    
    def write(self, cr, uid, ids, vals, context):
        result = super(project_work, self).write(cr, uid, ids, vals, context)
        if self.hr_analytic_timesheet_id:
            self.hr_analytic_timesheet_id.stop_time = self.stop_time
            self.hr_analytic_timesheet_id.start_time = self.date
        return result
"""
class project_work(models.Model):
    _inherit = "project.task.work"
    
    stop_time   = fields.Datetime(string="Stop time")
    #start_time  = fields.Datetime(string="Stop time")
    
    @api.multi
    def write(self, vals):
        result = super(project_work, self).write(vals)
        for record in self:
            if record.hr_analytic_timesheet_id:
                record.hr_analytic_timesheet_id.stop_time = record.stop_time
                record.hr_analytic_timesheet_id.start_time = record.date
        return result

    @api.one
    @api.onchange('date', 'stop_time')
    def onchange_timesheet_timer_start_stop_time(self):
        if self.date and self.stop_time:
            self.hours = (datetime.strptime(self.stop_time,
            #'%Y-%m-%d %H:%M:%S') - datetime.strptime(self.date, 
            #'%Y-%m-%d %H:%M:%S')).seconds / 3600.0
            tools.DEFAULT_SERVER_DATETIME_FORMAT) - datetime.strptime(self.date, 
            tools.DEFAULT_SERVER_DATETIME_FORMAT)).seconds / 3600.0

class project_task(models.Model):
    _inherit = "project.task"
    
    ss_button_inv = fields.Boolean(compute='_start_stop_button_invisible')
    
    @api.one
    def _start_stop_button_invisible(self):
        self.ss_button_inv = (self.env.user.id != self.user_id.id)
    
    @api.multi
    def check_started_work(self):
        for task in self:
            work = self.env['project.task.work'].search([['task_id', '=', task.id], ['hours', '=', 0]])
            if len(work) == 0:
                return True
        return False
        
    @api.one
    def start_stop_work(self, context={}, name=''):

        work = self.env['project.task.work'].search(['&',('user_id', '=', self.env.user.id), ('task_id', '=', self.id), ('hours', '=', 0)])

        #if self.env.user.id != self.user_id.id:
            #return False
        #work = self.env['project.task.work'].search([['task_id', '=', self.id], ['hours', '=', 0]])

        if len(work) == 0:
            #close old active works
            active_work = self.env['project.task.work'].search(['&',('user_id', '=', self.env.user.id), ('hours', '=', 0)])
            for w in active_work:
                try:
                    w.stop_time = fields.Datetime.now()
                    w.onchange_timesheet_timer_start_stop_time()
                    _logger.info("Stopped work on %s for task %s at time %s." % (w.name or '', w.task_id.name, w.stop_time or ''))
                except:
                    _logger.info("Error when attempting to stop work on %s for task %s." % (w.name or '', w.task_id.name))
            #create new work
            self.env['project.task.work'].create({
            'name': name,
            'date': fields.Datetime.now(),
            #'start_time': fields.Datetime.now(),
            'task_id': self.id,
            'hours': 0,
            'user_id': self.env.user.id,
            'company_id': self.company_id.id,
            })
        else:
            for w in work:
                w.stop_time = fields.Datetime.now()
                w.onchange_timesheet_timer_start_stop_time()
        return True

   
   # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
