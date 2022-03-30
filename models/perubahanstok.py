
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class PerubahanStok(models.Model):
    _name = 'imf.perubahanstok'
    _description = 'Model Perubahan Stok'

    tanggalPerubahanStok = fields.Date(string='Tanggal',default=fields.Date.today())
    gudang_id = fields.Many2one('imf.gudang', string='Nama Barang')
    kategori = fields.Selection(string='Kategori', selection=[('pembelian', 'Pembelian'), ('penjualan', 'Penjualan'), ('produksi', 'Produksi'), ('pemakaian', 'Pemakaian')])
    
    jumlahBarang = fields.Integer(string='Jumlah Barang')
    satuan = fields.Char(compute='_compute_satuan', string='Satuan', default="pcs")
   
    @api.depends('gudang_id')
    def _compute_satuan(self):
        for record in self:
            record.satuan = record.gudang_id.satuan
    
    @api.constrains('gudang_id')
    def _check_kodeProduksi(self):
        for record in self:
            stokGudang = sum(self.env['imf.gudang'].search([('id','=',record.gudang_id.id)]).mapped('stok'))
            if record.jumlahBarang and record.jumlahBarang > stokGudang and record.kategori == "penjualan"  :
                raise ValidationError("Error : Stok '" + record.gudang_id.name + "' tidak mencukupi")       
            elif record.jumlahBarang and record.jumlahBarang > stokGudang and record.kategori == "pemakaian": 
                raise ValidationError("Error : Stok '" + record.gudang_id.name + "' tidak mencukupi")  
    @api.model
    def create(self, values):
        result = super(PerubahanStok,self).create(values)
        if result.kategori == "pembelian" or result.kategori == "produksi":
            self.env['imf.gudang'].search([('id','=',result.gudang_id.id)]).write({'stok':result.gudang_id.stok + result.jumlahBarang})
        else:   
            result.jumlahBarang = -1 * result.jumlahBarang
            if result.jumlahBarang > 0 :
                result.jumlahBarang =result.jumlahBarang * -1
            self.env['imf.gudang'].search([('id','=',result.gudang_id.id)]).write({'stok':result.gudang_id.stok + (result.jumlahBarang)})    
                
        return result
    
    