from email.policy import default
from odoo import api, fields, models


class Akuntansi(models.Model):
    _name = 'imf.akuntansi'
    _description = 'Model Akuntansi'
    _order = 'id asc'


    name = fields.Char(string='Nama')
    date = fields.Date(string='Tanggal')
    debet = fields.Integer(string='Debet',default=0)
    kredit = fields.Integer(string='Kredit',default=0)
    saldo = fields.Integer(compute='_compute_saldo', string='Saldo')
    
    @api.depends('debet','kredit')
    def _compute_saldo(self):
        for record in self:
            dataSebelum = self.search_read([('id','<',record.id)],limit=1,order='date desc')
            saldoSebelum = dataSebelum[0]['saldo'] if dataSebelum else 0
            record.saldo = saldoSebelum + record.debet - record.kredit
        
