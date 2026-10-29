# -*- coding: utf-8 -*-
{
    'name': 'speciality',
    'summary': 'speciality',
    'author': 'Ibel technology',
    'website': 'https://ibeltechnology.sn',
    'category': 'category',
    'version': '20.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
         "base",
     ],
    'data' : [
        "security/ir.access.csv",
        "views/speciality_views.xml",
        "data/health_specialties.xml",
    ],
    'installable' : True,
    'auto_install': False,
    'application': False
}

