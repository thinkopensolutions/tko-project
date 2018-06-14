# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    Thinkopen Brasil
#    Copyright (C) Thinkopen Solutions Brasil (<http://www.tkobr.com>).
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
from odoo import models, fields, api, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    parent_id = fields.Many2one('project.project',u'Parent')


    @api.model
    def create(self, vals):
        res = super(ProjectProject, self).create(vals)
        if res.analytic_account_id and res.parent_id and res.parent_id.analytic_account_id:
            res.analytic_account_id.parent_id = res.parent_id.analytic_account_id.id

        return res

    @api.multi
    def write(self, vals):
        res = False 
        for record in self:
            res = super(ProjectProject, record).write(vals)
            if record.analytic_account_id and record.parent_id:
                #record.analytic_account_id.parent_id = record.parent_id.analytic_account_id.id
                self.env.cr.execute("update account_analytic_account set parent_id = %s where id = %s" %(record.parent_id.analytic_account_id.id, record.analytic_account_id.id))
        return res

