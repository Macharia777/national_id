import sys
sys.path.append('/home/ghost16/Learn/national_id/odoo-18.0/odoo-18.0/odoo')

from odoo import models, fields, api
from odoo.exceptions import UserError

class NationalIDApplication(models.Model):
    _name = 'national.id.application'
    _description = 'National ID Application'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Application Number', readonly=True, default='New')
    applicant_name = fields.Char('Full Name', required=True, tracking=True)
    birth_date = fields.Date('Date of Birth', required=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], required=True, tracking=True)
    phone = fields.Char('Phone Number', required=True, tracking=True)
    address = fields.Text('Residential Address', required=True, tracking=True)
    
    photo = fields.Binary('Passport Photo', required=True, attachment=True)
    lc_letter = fields.Binary('LC Reference Letter', required=True, attachment=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('stage1', 'First Approval'),
        ('stage2', 'Final Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft', tracking=True)
    
    stage1_approver_id = fields.Many2one('res.users', 'Stage 1 Approver', tracking=True)
    stage2_approver_id = fields.Many2one('res.users', 'Stage 2 Approver', tracking=True)

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].search([('code', '=', 'national.id.application')])
        if not sequence:
            raise UserError("The National ID Application sequence does not exist. Please define it in the system.")
        
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('national.id.application')
        return super(NationalIDApplication, self).create(vals)

    def action_submit(self):
        self.state = 'submitted'
        self.message_post(body="Application submitted for review")

    def action_stage1_approve(self):
        if self.state != 'submitted':
          raise UserError("Application must be submitted before Stage 1 approval.")
        self.state = 'stage1'
        self.stage1_approver_id = self.env.user.id
        self.message_post(body=f"Stage 1 approved by {self.env.user.name}")

    def action_stage2_approve(self):
        self.state = 'stage2'
        self.stage2_approver_id = self.env.user.id
        self.message_post(body=f"Stage 2 approved by {self.env.user.name}")

    def action_approve(self):
        self.state = 'approved'
        self.message_post(body="Application approved")

    def action_reject(self):
        self.state = 'rejected'
        self.message_post(body="Application rejected")
