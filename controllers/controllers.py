# -*- coding: utf-8 -*-
# from odoo import http


# class Indomomfood(http.Controller):
#     @http.route('/indomomfood/indomomfood/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/indomomfood/indomomfood/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('indomomfood.listing', {
#             'root': '/indomomfood/indomomfood',
#             'objects': http.request.env['indomomfood.indomomfood'].search([]),
#         })

#     @http.route('/indomomfood/indomomfood/objects/<model("indomomfood.indomomfood"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('indomomfood.object', {
#             'object': obj
#         })
