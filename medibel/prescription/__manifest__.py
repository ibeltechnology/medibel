{
    'name': 'Prescription',
    'summary': 'Custom website theme.',
    'version': '20.0.1.0.0',
    'category': 'Tools',
    'author': 'Ibel technology',
    'website': 'https://ibel.sn',
    'license': 'LGPL-3',
    'depends': [
        'base',
        # Add depends
        'mail',
        'patients',
        'medicaments_sn',
        'portal',
    ],
    'data': [
        "security/res_groups.xml",
        "security/ir.access.csv",
        "views/menus.xml",
        # Add XML files if needed
        "views/res_partner_views.xml",
        "report/prescription_report.xml",
        "views/medication_frequency_views.xml",
        "views/prescription_line_views.xml",
        "views/prescription_order_views.xml",
        "views/portal_entry.xml",
        "views/portal_templates.xml",
        "data/medication_frequency_data.xml",
    ],
    'images': ['prescription/static/description/cover.png'],
    'application': True,
    'assets': {

    },
}
