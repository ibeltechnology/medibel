{
    'name': 'Medicaments Sn',
    'summary': 'Custom website theme.',
    'version': '20.0.1.0.0',
    'category': 'Tools',
    'author': 'Ibel technology',
    'website': 'https://ibel.sn',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product',
        'account',
        # Add depends
    ],
    'data': [

        "security/ir.access.csv",
        "data/product_category_data.xml",
        'data/medicament_dci_data.xml',
        'data/medicament_data.xml',

        # Add XML files if needed
        "views/product_views.xml",
        "views/medicament_dci_views.xml",
        "views/medicament_views.xml",
    ],
    'images': ['medicaments_sn/static/description/cover.png'],
    'application': False,
    'assets': {

    },
}
