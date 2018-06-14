# -*- encoding: utf-8 -*-
from odoo import fields, api, models, _
from odoo.exceptions import Warning


class ProjectProject(models.Model):
    _inherit = 'project.project'

    team_id = fields.Many2one('project.team', u'Team')
    user_id_domain = fields.Selection([('nr', _('No Restriction')),
                                       ('pt', _(u"User's from Project Team")),
                                       ('at', _(u"User's from Action Line Team")),
                                       ('tt', _(u"User's from Task Team")),
                                       ], default='nr',
                                      string=u'Assigned To Restriction',
                                      help=u'This will restrict Assigned To in action lines basedon selection')


class ProjectTaskType(models.Model):
    _inherit = 'task.type'

    team_id = fields.Many2one('project.team', u'Team')


class ProjectTaskAction(models.Model):
    _inherit = 'project.task.action'

    team_id = fields.Many2one('project.team', u'Team')


class ProjectTaskActionLine(models.Model):
    _inherit = 'project.task.action.line'

    team_id = fields.Many2one('project.team', string=u'Team', compute='onchange_team', store=True)
    user_ids = fields.Many2many('res.users', 'task_action_line_project_team_users_rel',
                                'team_id', 'line_id', compute='get_authorized_users', store=True, string=u'Users')

    @api.one
    @api.depends('action_id', 'user_id', 'task_id.user_ids', 'project_id.user_id_domain', 'project_id.team_id')
    def get_authorized_users(self):

        domain = self.project_id.user_id_domain
        if domain == 'nr' or not self.project_id:
            users = self.env['res.users'].search([])
        elif domain == 'pt':
            users = self.project_id.team_id.user_ids
        elif domain == 'at':
            users = self.action_id.team_id.user_ids
        else:
            users = self.task_id.user_ids
        self.user_ids = [(6, 0, users.ids)]

    @api.one
    def self_assign(self):
        users = self.team_id.get_team_users()
        if self.env.uid in users:
            self.user_id = self.env.uid
        else:
            raise Warning(
                u"User %s doesn't belong to team %s or it's preant teams" % (self.env.user.name, self.team_id.name))

    # use separate method to get team_id
    # so that other modules which do not have fixed team
    # can compute team using this method
    def get_team_id(self):
        """
        Inherit this method if you want to use another team other than set in team_id field
        :return: database id of the team or False
        """
        return self.action_id and self.action_id.team_id and self.action_id.team_id.id or False

    @api.one
    @api.depends('action_id')
    def onchange_action(self):
        super(ProjectTaskActionLine, self).onchange_action()
        team_id = self.get_team_id()
        if not team_id:
            team_id = self.task_id and self.task_id.task_type_id and self.task_id.task_type_id.team_id \
                      and self.task_id.task_type_id.team_id.id or False
        if not team_id:
            team_id = self.task_id and self.task_id.project_id and self.task_id.project_id.team_id or False
        self.team_id = team_id
        # call oncange_team()
        # otherwise doesn't set the user based on team
        self.onchange_team()

    @api.one
    @api.depends('team_id', 'action_id')
    def onchange_team(self):
        if self.team_id:
            # self.team_id = self.team_id.id
            if self.team_id.type == 'b':
                self.user_id = False
            else:
                users = self.team_id.user_ids
                users_task_length = {}
                # make a dictionary with key, values as (user, tasks)
                # assign new line to the user which has min length of tasks
                if len(users):
                    for user in users:
                        users_task_length[user.id] = len(
                            self.search([('state', 'not in', ['d', 'c']), ('user_id', '=', user.id)]))

                    # get user with min length()
                    user_id = min(users_task_length, key=users_task_length.get)
                    self.user_id = user_id
