from odoo import models, fields

class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    x_locked = fields.Boolean(string="Locked Stage", default=False)
