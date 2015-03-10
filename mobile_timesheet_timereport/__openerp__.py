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
{
'name': 'Time Report',
'version': '0.1',
'category': 'Project',
'description': """
Time Report will help you to easily see a list of all your tasks through desktop or your mobile phone.
By choosing a task you will be able to read the description of the task, write work notification and the time spent on the task. 
Through Time Report you have even the option to set the status of the task to done. 

===================================================
""",
'author': 'Vertel AB',
'website': 'http://www.vertel.se',
'depends': ['project','project_timesheet','hr_timesheet','mobile_timesheet_menu'],
'data': ['mobile_timesheet_timereport_view.xml',
],
'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
