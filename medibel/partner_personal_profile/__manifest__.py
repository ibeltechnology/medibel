{
    "name": "Partner Personal Profile",
    "summary": "Extend res.partner with a Personal Profile tab",
    "version": "20.0.1.0.0",
    "category": "Medical",
    "author": "Abdourahmane Wone",
    "website": "https://doctibel.com",
    "license": "LGPL-3",
    "depends": ["base", "contacts","ibel_location",'ibel_gender',],
    "data": [
        "security/ir.access.csv",
        "views/res_partner_views.xml",
        "views/age_range_views.xml",
#        "data/ir_sequence.xml",
        "data/ir_cron.xml",
        "data/age_range_data.xml",
    ],
    "application": False,
}
