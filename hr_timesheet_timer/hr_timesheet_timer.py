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

import itertools
from lxml import etree
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

import logging

_logger = logging.getLogger(__name__)

class account_analytic_line(models.Model):
    _inherit = "account.analytic.line"
    
    start_time  = fields.Datetime(string="Start time", default=fields.Datetime.now())
    stop_time   = fields.Datetime(string="Stop time")
    
    @api.multi
    def onchange_stop_time(self, starttime, stoptime): #product_id, partner_id, inv_type, fposition_id, account_id):
        _logger.info('stop_time changed')
        return {'value': {'unit_amount': 42.0}}

    #@api.onchange('stop_time')
    #def on_stop_time_change(self):
    #    _logger.info('stop_time changed')
    #    self.unit_amount = 99.0
        #if self.stop_time - self.start_time > 0:
        #    self.unit_amount = self.stop_time - self.start_time

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
