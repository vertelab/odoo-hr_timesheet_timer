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
'name': 'Time Report Timer',
'version': '0.1',
'category': 'Project',
'description': """
Time Report will help you to easily see a list of all your tasks through desktop or your mobile phone.
Time Report will allow you to start and stop a task and in this way it will save the time you spent on the task.  
You have access to description of the task and you can write a work notification just by clicking on a task.
You can also change the status of the task to done. 

===================================================
""",
'author': 'Vertel AB',
'website': 'http://www.vertel.se',
'depends': ['project','hr_timesheet_timer','product','mobile_timesheet_menu'],
'data': ['mobile_timesheet_timer_view.xml',
],
'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
