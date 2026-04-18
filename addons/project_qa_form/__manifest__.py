{
    "name": "Project QA Rename",
    "version": "1.0.0",
    "license": "LGPL-3",

    'depends': ['project'],
    'depends': ['project', 'base'],
    'depends': ['project', 'mail'],

    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        "views/project_task_form_inherit_qcc_meter.xml",
        "views/project_task_form_inherit_qcc_minipillar.xml",
        'views/project_task_form_inherit_trench_802.xml',
    ],
    "installable": True,
    "application": False,

}
