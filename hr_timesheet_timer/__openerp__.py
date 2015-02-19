# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010-2012 OpenERP s.a. (<http://openerp.com>).
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


{
    'name': 'hr_timesheet_timer',
    'version': '0.1',
    'category': 'Human Resources',
    'description': """
Adding start and end time to timesheet.
===================================================
""",
    'author': 'Vertel AB',
    'website': 'http://www.vertel.se',
    'depends': ['hr_timesheet_sheet', 'hr_timesheet', 'project_timesheet'],
    'data': ['hr_timesheet_view.xml',
    ],

    'installable': True,
    
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
