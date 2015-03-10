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
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
from datetime import datetime
import werkzeug
import pytz


class website_check_in(http.Controller):
        
    @http.route(['/signin/<model("res.users"):user>', '/signin/<model("res.users"):user>/<string:clicked>', '/signin'], type='http', auth="user", website=True)
    def check(self, user=False, clicked=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        if not user:
            return werkzeug.utils.redirect("/signin/%s" %uid,302)
        if clicked:
            user.employee_ids[0].attendance_action_change()
        if post.get('signin_button',False): 
            user.employee_ids[0].attendance_action_change()
            
        last=user.employee_ids[0].last_sign
        # get user's timezone
        #user_pool = self.pool.get('res.users')
        #user = user_pool.browse(cr, SUPERUSER_ID, uid)
        tz = pytz.timezone(user.partner_id.tz or 'UTC')
        
        last = pytz.utc.localize(datetime.strptime(last or "1969-01-01 01:01:01", '%Y-%m-%d %H:%M:%S')).astimezone(tz).replace(tzinfo=None)
    
        ctx = {
            'user' : user,
            'signed_in': "Sign out" if user.employee_ids[0].state == 'present' else "Sign in",
            'last': last,             
            }
    

        return request.render('mobile_timesheet_attendance.check_in', ctx)
        
class hr_employee(models.Model):
    _inherit = ['hr.employee']
    
    def get_url(self):
        return self.pool['ir.config_parameter'].get_param(self.env.cr, SUPERUSER_ID, 'web.base.url')
    
    
    
    @api.multi
    def send_email(self):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        template = self.env.ref('website_attendance.email_template_website_att', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='hr.employee',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            #mark_invoice_as_sent=True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
