# -*- encoding: utf-8 -*-
{
    'name': 'NH Clinical activity types',
    'version': '0.1',
    'category': 'Clinical',
    'license': 'AGPL-3',
    'summary': '',
    'description': """    """,
    'author': 'Neova Health',
    'website': 'http://www.neovahealth.co.uk/',
    'depends': ['nh_clinical','project','hr'],
    'data': [
             'views/views.xml',
             'security/notif/ir.model.access.csv',
             'security/obs/ir.model.access.csv',
             'security/params/ir.model.access.csv',],
    'demo': [],
    'css': [],
    'js': [],
    'qweb': [],
    'images': [],
    'application': True,
    'installable': True,
    'active': False,
}