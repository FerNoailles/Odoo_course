# -*- coding: utf-8 -*-
# © 2015 Fernando Vasconcellos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

class HelpdeskTeam(models.Model):
    _name = 'helpdesk.ticket.team'

    #THERE IS 3 WAYS TO DETERMINE THE CURRENT COMPANY FOR A USER:
    """
    ->    self.env['res.company']._company_default_get()    #GOIN THROUGH A METHOD IN res.company

    ->    self.env['res.users']._get_company()              #METHOD FROM res.user

          ^__ TWO WAYS IN WHICH WE DO IT VIA MUCH MORE STATIC METHODS

    ->    self.env.user.company_id                          #MUCH LIGHTER

    ¿Odoo 10 only?
    """
    def _get_default_company_id(self):
        return self.env['res.users']._get_company()

    name = fields.Char(
        string = "Name",
        required = True,
    )

    user_ids = fields.Many2Many(
        comodel_name = 'res.users',     # RELATED MODEL
        string = "Members",
    )

    active = fields.Boolean(
        default = True
    )

    category_ids = fields.Many2many(
        comodel_name = 'helpdesk.ticket.category',
        string = 'Category',
    )

    company_id = fields.Many2one(        # THE EQUIVALENT TO A FOREIGN KEY
        comodel_name = 'res.users',
        string = 'Company',
        default = _get_default_company_id,
    )

    