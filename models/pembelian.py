from odoo import api, fields, models


class Pembelian(models.Model):
    _name = 'imf.pembelian'
    _description = 'Model Pembelian'

    tanggalTransaksi = fields.Date(string='Tanggal', default= fields.Date.today())
    
    gudang_id = fields.Many2one('imf.gudang', string='Nama Barang')
    harga = fields.Integer(compute='_compute_harga', string='Harga')

    jumlahBarang = fields.Integer(string='Jumlah Barang')
    satuan = fields.Char(compute='_compute_satuan', string='Satuan', default="pcs")
    totalPengeluaran = fields.Integer(compute='_compute_totalPengeluaran', string='Total Pengeluaran')
    terhitung = fields.Selection(string='Terhitung', selection=[('ya', 'Ya'), ('tidak', 'tidak')], readonly=True, default='tidak')
    
    @api.depends('gudang_id')
    def _compute_satuan(self):
        for record in self:
            record.satuan = record.gudang_id.satuan


    @api.depends('gudang_id','jumlahBarang')
    def _compute_totalPengeluaran(self):
        for record in self: 
            record.totalPengeluaran = record.harga * record.jumlahBarang
        
    @api.depends('gudang_id')
    def _compute_harga(self):
        for record in self:
            record.harga = record.gudang_id.harga
        
    @api.model
    def create(self, values):
        result = super(Pembelian,self).create(values)
        self.env['imf.perubahanstok'].create({'tanggalPerubahanStok':result.tanggalTransaksi,'gudang_id':result.gudang_id.id,'kategori':'pembelian', 'jumlahBarang':result.jumlahBarang})    
        return result

    def unlink(self):
        for record in self:
            self.env['imf.perubahanstok'].search([('tanggalPerubahanStok','=',record.tanggalTransaksi),('kategori','=','pembelian'),('jumlahBarang','=',record.jumlahBarang),('gudang_id','=',record.gudang_id.id)],limit=1).unlink()
            self.env['imf.gudang'].search([('id','=',record.gudang_id.id)]).write({'stok':record.gudang_id.stok - (record.jumlahBarang)})
        return super(Pembelian, self).unlink()

    def toAkuntansi(self, **kwargs):
        for record in self:
            self.env['imf.akuntansi'].create({'name':'Pembelian ' + str(record.gudang_id.name) + ' ' + str(record.jumlahBarang) + str(record.satuan),
                                                'date' : record.tanggalTransaksi,
                                                'kredit'  : record.totalPengeluaran
                                                })
            record.terhitung = 'ya'