# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
import openerp.tools
import string
import werkzeug
import logging
import math
_logger = logging.getLogger(__name__)

class controller(http.Controller):
    
    @http.route(['/timereport/gtd/list'], type='http', auth="user", website=True)
    def gtd_list(self, **post):
        ctx = {
            'longitude' : post.get("longitude") if post else None,
            'latitude' : post.get("latitude") if post else None,
            'redirect' : '/timereport/gtd',
            'update_position' : not post.get("update_position", "True") == "True",
            #~ 'calendar_id' : calendar_id.name if ('resource_calendar_attendace.dayofweek')>= 0 or ('resource_calendar_attendace.dayofweek')<= 4 else None
            }
        stage = request.env.ref("project.project_tt_deployment")
        ctx['tasks']= request.env['project.task'].search(['&',("user_id","=",request.uid),("stage_id.id","!=",stage.id)], order='sequence').sorted(key=lambda r: r.context_id.name)
        return request.render('project_gtd_context.gtd_context', ctx)

    @http.route(['/timereport/gtd'], type='http', auth="user", website=True)
    def get_location(self, **post):
        ctx = {
            'longitude' : post.get("longitude") if post else None,
            'latitude' : post.get("latitude") if post else None,
            'redirect' : '/timereport/gtd',
            'update_position' : not post.get("update_position", "True") == "True",
        }
        _logger.info('post: %s long: %s lat: %s' % (post, ctx['longitude'], ctx['latitude']))
        if ctx["update_position"]:
            stage = request.env.ref("project.project_tt_deployment")
            contexts_list = []
            if ctx["longitude"] and ctx["latitude"]:
                contexts = request.env["project.gtd.context"].search([])
                _logger.info(contexts)
                for record in contexts:
                    if record.check_position(float(ctx["longitude"]), float(ctx["latitude"]), 0.01):
                        contexts_list.append(record.id)
                _logger.info(contexts_list)
            ctx['tasks']= request.env['project.task'].search(['&',("context_id","in",contexts_list),('user_id','=',request.uid),("stage_id.id","!=",stage.id)], order='sequence')
            
            return request.render('project_gtd_context.gtd_context', ctx)
            
        return request.render('project_gtd_context.get_location', ctx) 

    @http.route(['/timereport/gtd/<model("project.gtd.context"):gtd_context>'], type='http', auth="user", website=True)
    def gtd_context(self, gtd_context=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        stage = request.env.ref("project.project_tt_deployment")
        ctx = {
            'context' : gtd_context,
            'contexts' : request.env['project.gtd.context'].search([]),
            'tasks': request.env['project.task'].search(['&',('context_id','=',gtd_context and gtd_context.id),('user_id','=',uid),("stage_id.id","!=",stage.id)]),
            'redirect' : '/timereport/gtd/%s' % gtd_context.id,
            }
    
        return request.render('project_gtd_context.gtd_context', ctx)
        
    @http.route(['/timereport/gtd/time/<model("project.gtd.timebox"):gtd_timebox>'], type='http', auth="user", website=True)
    def gtd_timebox(self, gtd_timebox=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        stage = request.env.ref("project.project_tt_deployment")
        ctx = {
            'timebox' : gtd_timebox,
            'timeboxes' : request.env['project.gtd.timebox'].search([]),
            'tasks': request.env['project.task'].search(['&',('timebox_id','=',gtd_timebox and gtd_timebox.id),('user_id','=',uid),("stage_id.id","!=",stage.id)]),
            'redirect' : '/timereport/gtd/time/%s' % gtd_timebox.id,
            }
    
        return request.render('project_gtd_context.gtd_context', ctx)

class project_gtd_context(models.Model):
    _inherit = "project.gtd.context"

    latitude = fields.Float(string = "Lat")
    longitude = fields.Float(string = "Long")
    calendar_id = fields.One2many("resource.calendar", inverse_name="gtd_calendar")
    task_ids = fields.Many2one("project.task", inverse_name="gtd_context_id")
    
    def check_position(self, longitude, latitude, distance):
        if self.longitude and self.latitude:
            if math.sqrt(math.pow(longitude-self.longitude, 2)+math.pow(latitude-self.latitude, 2)) <= distance:
                return True
        return False

class project_task(models.Model):
    _inherit= "project.task"    
 
    gtd_context_id = fields.One2many("project.gtd.context", inverse_name="task_ids")

class calendar(models.Model):
    _inherit="resource.calendar"
    
    gtd_calendar = fields.Many2one("project.gtd.context", inverse_name="calendar_id")
    
    #~ start_time = fields.Datetime('Start Date', select="1")
    #~ stop_time = fields.Datetime('Stop Date', select="1")
    #~ boo = fields.Boolean(compute="loo", default=False)
    #~ 

    #~ def loo(self):
        #~ if self.date_start:
            #~ if int(self.date_start).weekday() >= 0 and int(self.date_start).weekday() <= 4:
                #~ self.boo = True
