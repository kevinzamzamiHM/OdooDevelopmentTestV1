from email.policy import default
from odoo import api, fields, models


class Penjualan(models.Model):
    _name = 'imf.penjualan'
    _description = 'Model Penjualan'

    tanggalTransaksi = fields.Date(string='Tanggal',default= fields.Date.today())
    
    
    reseller_id = fields.Many2one('imf.reseller', string='Reseller')
    gudang_id = fields.Many2one('imf.gudang', string='Barang',domain=[('kategori','=','produk')])
    harga = fields.Integer(compute='_compute_harga', string='Harga')
    jumlahBarang = fields.Integer(string='Jumlah Terjual')
    satuan = fields.Char(compute='_compute_satuan', string='Satuan', default="pcs")
    totalPendapatan = fields.Integer(compute='_compute_totalPendapatan', string='Total')
    terhitung = fields.Selection(string='Terhitung', selection=[('ya', 'Ya'), ('tidak', 'tidak')], readonly=True, default='tidak')
   
    @api.depends('gudang_id')
    def _compute_satuan(self):
        for record in self:
            record.satuan = record.gudang_id.satuan

    @api.depends('gudang_id','jumlahBarang')
    def _compute_totalPendapatan(self):
        for record in self:
            record.totalPendapatan = record.harga * record.jumlahBarang
    
    @api.depends('gudang_id')
    def _compute_harga(self):
        for record in self:
            record.harga = record.gudang_id.hargaJual

    @api.model
    def create(self, values):
        result = super(Penjualan,self).create(values)
        self.env['imf.perubahanstok'].create({'tanggalPerubahanStok':result.tanggalTransaksi,'gudang_id':result.gudang_id.id,'kategori':'penjualan', 'jumlahBarang':result.jumlahBarang})    
        return result

    def unlink(self):
        for record in self:
            self.env['imf.perubahanstok'].search([('tanggalPerubahanStok','=',record.tanggalTransaksi),('kategori','=','penjualan'),('jumlahBarang','=',record.jumlahBarang),('gudang_id','=',record.gudang_id.id)],limit=1).unlink()
            self.env['imf.gudang'].search([('id','=',record.gudang_id.id)]).write({'stok':record.gudang_id.stok + (record.jumlahBarang)})
        return super(Penjualan, self).unlink()
    
    def toAkuntansi(self, **kwargs):
        for record in self:
            self.env['imf.akuntansi'].create({'name':'Penjualan ' + str(record.gudang_id.name) + ' ' + str(record.jumlahBarang) + str(record.satuan),
                                                'date' : record.tanggalTransaksi,
                                                'debet'  : record.totalPendapatan
                                                })
            record.terhitung = 'ya'