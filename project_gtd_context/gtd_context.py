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
    
    @http.route(['/gtd', '/gtd/list'], type='http', auth="user", website=True)
    def gtd_list(self, **post):
        ctx = {
            'longitude' : post.get("longitude") if post else None,
            'latitude' : post.get("latitude") if post else None,
            }
        stage = request.env.ref("project.project_tt_deployment")
        if ctx["longitude"] and ctx["latitude"]:
            contexts = request.env["project.gtd.context"].search([])
            _logger.info(contexts)
            contexts_list = []
            for record in contexts:
                if record.check_position(float(ctx["longitude"]), float(ctx["latitude"]), 0.01):
                    contexts_list.append(record.id)
            _logger.info(contexts_list)
            ctx['tasks']= request.env['project.task'].search(['&',("context_id","in",contexts_list),("stage_id.id","!=",stage.id)], order='sequence')
        else:
            ctx['tasks']= request.env['project.task'].search(['&',("user_id","=",request.uid),("stage_id.id","!=",stage.id)], order='sequence')

        return request.render('project_gtd_context.gtd_context', ctx)

    @http.route(['/gtd/<model("project.task"):task>'], type='http', auth="user", website=True)
    def timereport_form(self, task=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        
        if request.httprequest.method == 'POST':
            _logger.warning("This is gtd post %s " % (post))
            
            return werkzeug.utils.redirect("/gtd/%s" %user.id)
            
        ctx = {
            'task': task,
            }
    

        return request.render('project_gtd_context.gtd_task_form', ctx)

class project_gtd_context(models.Model):
    _inherit = "project.gtd.context"

    latitude = fields.Float(string = "Lat")
    longitude = fields.Float(string = "Long")
    gps_base_base_ids = fields.One2many("gps_base.base", inverse_name="project_gtd_context_id")
    start_time = fields.Datetime('Start Date', select="1")
    stop_time = fields.Datetime('Stop Date', select="1")
    task_ids = fields.Many2one("project.task", inverse_name="gtd_context_id")
    
    def check_position(self, longitude, latitude, distance):
        if self.longitude and self.latitude:
            if math.sqrt(math.pow(longitude-self.longitude, 2)+math.pow(latitude-self.latitude, 2)) <= distance:
                return True
        return False
    
class gps_base_base(models.Model):
    _inherit = "gps_base.base"
    
    project_gtd_context_id = fields.Many2one("project.gtd.context")

class project_task(models.Model):
    _inherit= "project.task"
    
    gtd_context_id = fields.One2many("project.gtd.context", inverse_name="task_ids")


            
            
