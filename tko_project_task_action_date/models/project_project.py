# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    ThinkOpen Solutions Brasil
#    Copyright (C) Thinkopen Solutions <http://www.tkobr.com>.
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

from odoo import models, api, fields
from odoo.exceptions import UserError
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DT


class ProjectTaskActon(models.Model):
    _inherit = 'project.task.action'

    edit_expected_date = fields.Boolean("Edit Expected Date?", default=True)


class ProjectTaskActonLine(models.Model):
    _inherit = 'project.task.action.line'

    user_expected_date = fields.Date(u'Expected Date')
    edit_expected_date = fields.Boolean(string="Edit Expected Date?", related="action_id.edit_expected_date")

    @api.onchange('user_expected_date')
    def onchagne(self):
        self.expected_date = self.user_expected_date

    @api.constrains('user_expected_date')
    def check_user_expected_date(self):
        for line in self:
            if line.user_expected_date and line.task_id.date_deadline:
                if datetime.strptime(line.user_expected_date, DT) > datetime.strptime(line.task_id.date_deadline, DT):
                    raise UserError("Expected date %s must be less than date deadline!" % line.user_expected_date)
