{
    'name': 'Patients',
    'summary': 'Medical Records Management',
    'version': '20.0.1.0.0',
    'category': 'Medical',
    'author': 'Abdourahmane Wone',
    'website': 'https://doctibel.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'portal',
        'ibel_gender',
        'partner_personal_profile',
        'medical_pathology',
        'medical_specialty',
        
    ],
    'data': [
        "security/security.xml",
        "security/ir.access.csv",
        "views/patient_views.xml",
        "views/res_partner_views.xml",
        "views/disease_views.xml",
        "views/region_views.xml",
        "views/departement_views.xml",
        "views/arrondissement_views.xml",
        "views/commune_views.xml",
        "views/res_config_settings_views.xml",
        "views/portal_templates.xml",
        # Add XML files if needed
    ],
    'images': ['patient/static/description/cover.png'],
    'application': True,
    'assets': {

    },
}
