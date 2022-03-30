from email.policy import default
from odoo import api, fields, models


class Gudang(models.Model):
    _name = 'imf.gudang'
    _description = 'Model Gudang'

    name = fields.Char(string='Nama Barang')
    kategori = fields.Selection(string='Kategori', selection=[('produk', 'Produk'), ('bahan - bahan', 'Bahan - Bahan'), ('alat', 'Alat')])
    
    satuan = fields.Selection(string='Satuan', selection=[('pcs', 'pcs'),('dus', 'Dus'),('liter', 'Liter'), ('1/2 liter', '1/2 Liter'),('kg', 'Kg'),('m', 'm'),('cm', 'cm')])
    
    harga = fields.Integer(string='Harga Pokok')
    hargaJual = fields.Integer(string='Harga Jual')
    
    deskripsi = fields.Char(string='Deskripsi Barang')
    letak = fields.Char(string='Letak Barang', default="Gudang Utama")
    stok = fields.Integer(string='Stok', default="0", readonly=True)
    perubahanstok_ids = fields.One2many('imf.perubahanstok', 'gudang_id', string='Perubahan Stok')
    
    