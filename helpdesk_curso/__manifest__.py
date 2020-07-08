{
    'name': 'Helpdesk Factor Libre',
    'summary': "Manage systems from helpdesk course",
    'version': '11.0.1.0.1',
    'author': "Fernando Vasoncellos",
    'license': "AGPL-3",
    'maintainer': 'Fernando Vasconcellos',
    'category': 'Helpdesk',
    'website': 'https://odoo-community.org/',
    'depends': ['mail'],
    'data':[
        'data/helpdesk_data.xml',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_ticket_tag_views.xml',
        'views/inherit_res_partner_views.xml',
        'security/helpdesk_security.xml',
        ],
    'installable': True,
}