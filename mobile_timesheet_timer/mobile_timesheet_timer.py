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
        
    @http.route(['/treport/<model("res.users"):user>', '/treport/<model("res.users"):user>/list', '/treport'], type='http', auth="user", website=True)
    def timereport_list(self, user=False, clicked=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        if not user:
            return werkzeug.utils.redirect("/treport/%s/list" %uid,302)

        ctx = {
            'user' : user,
            'tasks': request.registry.get('project.task').browse(cr,uid,request.registry.get('project.task').search(cr,uid,['&',("user_id","=",user.id),("stage_id.name","!=","Done")], order='priority desc')
            ,context=context),
            }
    

        return request.render('mobile_timesheet_timer.project_timereport', ctx)


    @http.route(['/treport/<model("res.users"):user>/<model("project.task"):task>/<int:start>', ], type='http', auth="user", website=True)
    def timereport_form(self, user=False, task=False, start=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        if not user:
            return werkzeug.utils.redirect("/treport/%s/form" %uid,302)
        works=pool.get('project.task.work').search(cr,uid,['&',('task_id','=',task.id),('hours', '=', 0)])
        if request.httprequest.method == 'POST':
            _logger.warning(_("This is timereport post %s ") % (post))
            
            if start == 1:
                task.start_stop_work(context, post.get('name'))
                return werkzeug.utils.redirect("/treport/%s" %user.id) 
            
            if len (works)!=0:
                pool.get('project.task.work').browse(cr,uid,works[0]).name=post.get('name')
                
            if start == 2:
                stage=pool.get('project.task.type').search(cr,uid, ['&',('project_ids','=',task.project_id.id),('name', '=', 'Done')])
                #if the statement above is correct return the first element in the list stage.
                if len(stage) > 0:
                    task.stage_id=stage[0]
            return werkzeug.utils.redirect("/treport/%s" %user.id) 

        ctx = {
            'user': user,
            'task': task, 
            'work': False if len (works)==0 else pool.get('project.task.work').browse(cr,uid,works[0]), 
            }
    

        return request.render('mobile_timesheet_timer.project_timereport_form', ctx)
