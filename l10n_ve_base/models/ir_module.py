from odoo import fields, models


class IrModule(models.Model):
    _inherit = "ir.module.module"

    binaural = fields.Boolean(default=False)
