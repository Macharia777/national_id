{
    'name': 'National ID Application',
    'version': '1.0',
    'category': 'Government',
    'summary': 'Process National ID Applications',
    'description': """
        Module for processing National ID applications with approval workflow
    """,
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/national_id_views.xml',
        # 'data/sequences.xml',
    ],
    'installable': True,
    'application': True,
}
