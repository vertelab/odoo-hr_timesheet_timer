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

{
    'name': 'Punch Clock',
    'version': '0.1',
    'category': 'Sales',
    'description': """
            Using Punch Clock you will be able to sign in and out through your mobile phone. 
===================================================
""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': ['base','mail', 'website', 'hr_attendance','mobile_timesheet_menu'],
    'data': ['mobile_timesheet_attendance_view.xml',
    ],

    'installable': True,
    
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
