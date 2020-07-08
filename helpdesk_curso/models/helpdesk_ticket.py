# -*- coding: utf-8 -*-
# © 2015 Fernando Vasconcellos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, _, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_stage_id(self):
        return self.env['helpdesk.ticket.stage'].search([], limit=1).id

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['helpdesk.ticket.stage'].search([])
        return stage_ids
    
    name = fields.Char(
        string = 'Tittle',
        required = True,
    )

    description = fields.Html(
        string = 'Description',
    )

    priority = fields.Selection([
        ('zero',_('Zero')),
        ('low',_('Low')),
        ('medium',_('Medium')),
        ('high',_('High')),
        ],
        string="Priority",
        default="medium")

    assigned_date = fields.Datetime(
        string='Start Date',
        compute='_compute_assigned_date',
        store=True,
    )

    end_date = fields.Date(string='End Date',required=True)

    user_id = fields.Many2one(
        string = "Assigned to",
        comodel_name = "res.users",
        ondelete = "restrict",
    )

    partner_id = fields.Many2one(
        string = "Customer",
        comodel_name = "res.partner",
        ondelete = "restrict",
    )

    customer_name  =fields.Char(
        string = "Customer name",
    )

    customer_mail  =fields.Char(
        string = "Customer mail",     
    )

    tag_ids = fields.Many2many(
        name            = "Tags",
        comodel_name    = "helpdesk.ticket.tag",
    )

    color = fields.Integer(
        default = 0,
        compute = '_compute_deadline',
    )

    stage_id = fields.Many2one(
        'helpdesk.ticket.stage',
        string='Stage',
        group_expand='_read_group_stage_ids',
        default=_get_default_stage_id,
        track_visibility='onchange',
    )

    @api.multi
    def assign_to_me (self):
        self.write({
            'user_id' : self.env.user.id
        })

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for record in self:
            partner = record.partner_id
            if partner:
                record.update({
                    'customer_name' : partner.name,
                    'customer_mail' : partner.email,
                })
    
    @api.depends('user_id')
    def _compute_assigned_date(self):
        for tickets in self:
            tickets.assigned_date = fields.Datetime.now()

    @api.model
    def create(self,vals):
        if vals.get("partner_id") and (
            "customer_name" not in vals or "customer_mail" not in vals
        ):
            partner = self.env("res.partner").browse(vals["partner_id"])
            vals.setdefault("customer_name", partner.name)
            vals.setdefault("customer_mail", partner.email)
        
        res = super().create(vals)
        return res

    @api.model
    def _compute_deadline(self):
        for record in self:
            dnow = datetime.now()
            dout = datetime.strptime(record.end_date, '%Y-%m-%d')
            if  ( ( dout - dnow ).days  < 0 ):
                if ( int(record.stage_id) < 17 ):
                    record.update({
                        'color' : 1
                    })
            else:
                if( abs( ( dout - dnow ).days )  > 3 ):
                    if ( int(record.stage_id) < 17 ):
                        record.update({
                            'color' : 10
                        })
                else:
                    if ( int(record.stage_id) < 17 ):
                        record.update({
                            'color' : 3
                        })