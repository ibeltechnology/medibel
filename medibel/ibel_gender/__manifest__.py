{
    'name': 'Ibel Gender',
    'summary': 'Custom website theme.',
    'version': '20.0.1.0.0',
    'category': 'Tools',
    'author': 'Ibel technology',
    'website': 'https://ibel.sn',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'data': [

        "security/ir.access.csv",

        # Add XML files if needed
        "views/medical_gender_views.xml",
        "data/medical_gender_data.xml",
    ],
    'images': ['ibel_gender/static/description/cover.png'],
    'application': False,
    'assets': {

    },
}
