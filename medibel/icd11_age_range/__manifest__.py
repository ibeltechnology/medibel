{
    'name': 'Icd11 Age Range',
    'summary': 'Add age range to pathologies.',
    'version': '20.0.1.0.0',
    'category': 'Tools',
    'author': 'Abdourahmane Wone',
    'website': 'https://doctibel.com',
    'license': 'LGPL-3',
    'depends': [
        'icd11',
        'medical_pathology',        
        'partner_personal_profile',
        'patients',
        
        
    ],
    'data': [

        "security/ir.access.csv",
        "views/views.xml",
        'data/pathology.xml',

    ],
    'application': False,

}
