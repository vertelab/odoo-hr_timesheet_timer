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
        
    @http.route(['/timereport/<model("res.users"):user>', '/timereport/<model("res.users"):user>/list', '/timereport'], type='http', auth="user", website=True)
    def timereport_list(self, user=False, clicked=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        if not user:
            return werkzeug.utils.redirect("/timereport/%s/list" %uid,302)
           
        ctx = {
            'user' : user,
            'tasks': request.registry.get('project.task').browse(cr,uid,request.registry.get('project.task').search(cr,uid,['&',("user_id","=",user.id),("stage_id.name","!=","Done")], order='priority desc')
            ,context=context),
            }
    

        return request.render('mobile_timesheet_timereport.project_timereport', ctx)
        
    @http.route(['/timereport/<model("res.users"):user>/<model("project.task"):task>/<int:start>'], type='http', auth="user", website=True)
    def timereport_form(self, user=False, task=False, start=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        if not user:
            return werkzeug.utils.redirect("/timereport/%s/form" %uid,302)
            
        if request.httprequest.method == 'POST':
            _logger.warning("This is timereport post %s " % (post))
            
            if start==1:
                work_id = pool.get('project.task.work').create(cr,uid,{
                    'task_id':task.id, 
                    'name': post.get('name'),
                    #'work': post.get('work'),
                    'hours': self.checkTimeString(post.get('hours')),
                    #'date': partner.property_account_position and partner.property_account_position.id or False,
                    'user_id': user.id,
                    })
            
            elif start == 2:
                stage=pool.get('project.task.type').search(cr,uid, ['&',('project_ids','=',task.project_id.id),('name', '=', 'Done')])
                #if the statement above is correct return the first element in the list stage.
                if len(stage) > 0:
                    task.stage_id=stage[0]
            
            return werkzeug.utils.redirect("/timereport/%s" %user.id)
            
        ctx = {
            'user' : user,
            'task': task,
            }
    

        return request.render('mobile_timesheet_timereport.project_timereport_form', ctx)

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
