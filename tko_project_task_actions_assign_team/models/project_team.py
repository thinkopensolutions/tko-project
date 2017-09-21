# -*- encoding: utf-8 -*-
from odoo import fields, api, models, _


class ProjectTeam(models.Model):
    _name = 'project.team'

    name = fields.Char('Name', required=True)
    type = fields.Selection([('b', u'Bucket'), ('p', u'Prorate')], default='p', required=True)
    parent_id = fields.Many2one('project.team', u'Parent')
    manager_id = fields.Many2one('res.users', u'Manager')
    user_ids = fields.Many2many('res.users', 'project_team_users_rel', 'team_id', 'user_id', string=u'Users')


    def get_team_users(self, users= []):
        users += self.user_ids.ids
        if self.manager_id:
            users.append(self.manager_id.id)
        if self.parent_id:
            self.parent_id.get_team_users(users)
        return list(set(users))



