from email.policy import default
from tracemalloc import DomainFilter
from odoo import api, fields, models
from odoo.exceptions import ValidationError
        

class Produksi(models.Model):
    _name = 'imf.produksi'
    _description = 'Model Produksi'

    name = fields.Char(string='Kode Produksi',default="kode_namaproduk")
    gudang_id = fields.Many2one('imf.gudang', string='Nama Produk', domain=[('kategori','=','produk')])
    tanggalProduksi = fields.Date(string='Tanggal Produksi', default=fields.Date.today())
    hargaProduksi = fields.Integer(compute='_compute_hargaProduksi', string='Biaya Produksi Satuan')
    stok = fields.Integer(string='Jumlah Produksi')
    hargaProduksiTotal = fields.Integer(compute='_compute_hargaProduksiTotal', string='Biaya Produksi Total')
    deskripsi = fields.Char(string='Deskripsi Produksi')
    
    @api.constrains('name')
    def _check_kodeProduksi(self):
        for record in self:
            recordIdKodeProduksi = self.env['imf.produksi'].search([('name','=',record.name)]).mapped('id')
            if len(recordIdKodeProduksi) > 1 :
                raise ValidationError("Error : Kode Produksi '" + record.name + "' sudah pernah dibuat.")        
    
    @api.depends('gudang_id','stok')
    def _compute_hargaProduksiTotal(self):
        for record in self:
            record.hargaProduksiTotal = record.hargaProduksi * record.stok


    @api.depends('gudang_id')
    def _compute_hargaProduksi(self):
        for record in self:
            record.hargaProduksi = record.gudang_id.harga

    @api.model
    def create(self, values):
        result = super(Produksi,self).create(values)
        if result :
            self.env['imf.perubahanstok'].create({'gudang_id':result.gudang_id.id,'kategori':'produksi', 'jumlahBarang':result.stok})
        return result

    def unlink(self):
        for record in self:
            self.env['imf.perubahanstok'].search([('tanggalPerubahanStok','=',record.tanggalProduksi),('kategori','=','produksi'),('jumlahBarang','=',record.stok),('gudang_id','=',record.gudang_id.id)],limit=1).unlink()
            self.env['imf.gudang'].search([('id','=',record.gudang_id.id)]).write({'stok':record.gudang_id.stok - (record.stok)})
        return super(Produksi, self).unlink()
    
    
    
