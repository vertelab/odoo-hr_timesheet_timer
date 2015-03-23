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
_logger = logging.getLogger(__name__)

class project_timereport(http.Controller):
        
    @http.route(['/timereport', '/timereport/list'], type='http', auth="user", website=True)
    def timereport_list(self, **post):
        stage=request.env.ref('project.project_tt_deployment')
           
        ctx = {
            'tasks': request.env['project.task'].search(['&',("user_id","=",request.uid),("stage_id.id","!=",stage.id)], order='sequence'),
            }

        return request.render('mobile_timesheet_timereport.project_timereport', ctx)
        
    @http.route(['/timereport/<model("project.task"):task>'], type='http', auth="user", website=True)
    def timereport_form(self, task=False, **post):          
        if request.httprequest.method == 'POST':
            _logger.warning("This is timereport post %s " % (post))
            
            work_id = request.env['project.task.work'].create({
                'task_id':task.id, 
                'name': post.get('name'),
                #'work': post.get('work'),
                'hours': self.checkTimeString(post.get('hours')),
                #'date': partner.property_account_position and partner.property_account_position.id or False,
                'user_id': request.uid,
                })
            
            if post.get("done"):
                task.stage_id = request.env.ref('project.project_tt_deployment').id
            
            return werkzeug.utils.redirect("/timereport/list" )
            
        return request.render('mobile_timesheet_timereport.project_timereport_form',{'task':task})

    def checkTimeString(self,string_time):
        try:
            split_string = string_time.split(":")
        except:
            print "Wrong format, must be a string"
            return False
            
            #len(split_string)==2 == hh:mm      split_string[0] = hours      split_string[1] = minutes
        if len(split_string) ==2 and 0 < len(split_string[0]) < 3 and len(split_string[1]) == 2 :
                
            #check 'string' hour
            if int(split_string[0]) < 0 or int(split_string[0]) > 23:
                return False
      
            #check 'string' minute
            if int(split_string[1]) < 0 or int(split_string[1]) > 59:
                return False
        else: 
            return False
            
        return float(split_string[1])/60+float(split_string[0])
