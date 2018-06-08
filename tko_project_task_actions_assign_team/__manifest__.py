# © 2017 TKO <http://tko.tko-br.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Project Task Actions Assign Teams',
    'summary': '',
    'description': 'Manage teams on projects, tasks, and actions, '
                   'set assigned to on action lines',
    'author': 'TKO',
    'category': 'Project',
    'license': 'AGPL-3',
    'website': 'http://tko.tko-br.com',
    'version': '10.0.0.0.0',
    'application': False,
    'installable': True,

    'auto_install': False,
    'depends': [
        'tko_project_task_actions_assign',
    ],
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'init_xml': [],
    'update_xml': [],
    'css': [],
    'demo_xml': [],
    'test': [],
    'data': [
        'security/ir.model.access.csv',
        'wizard/action_line_user_view.xml',
        'views/project_task_view.xml',
        'views/project_team_view.xml',
    ],
}
