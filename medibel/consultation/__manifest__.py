{
    'name': 'Consultation',
    'summary': 'Custom website theme.',
    'version': '20.0.1.0.0',
    'category': 'Tools',
    'author': 'Ibel technology',
    'website': 'https://ibel.sn',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'patients',
    ],
    'data': [
        "security/security.xml",
        "security/ir.access.csv",
        "views/menus.xml",
        # Add XML files if needed
        "views/consultation_evaluation_views.xml",
    ],
    'images': ['consultation/static/description/cover.png'],
    'application': True,
    'assets': {

    },
}
