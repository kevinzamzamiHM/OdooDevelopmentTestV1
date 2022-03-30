from odoo import api, fields, models


class Reseller(models.Model):
    _name = 'imf.reseller'
    _description = 'Model Reseller'

    name = fields.Char(string='Name')
    pic = fields.Char(string='Person in Charge')
    alamat = fields.Char(string='Alamat')
    status = fields.Selection(string='Status', selection=[('aktif', 'Aktif'), ('non aktif', 'Non Aktif'),])
    

    