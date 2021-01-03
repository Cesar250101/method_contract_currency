# -*- coding: utf-8 -*-
from odoo import http

# class MethodContractCurrency(http.Controller):
#     @http.route('/method_contract_currency/method_contract_currency/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/method_contract_currency/method_contract_currency/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('method_contract_currency.listing', {
#             'root': '/method_contract_currency/method_contract_currency',
#             'objects': http.request.env['method_contract_currency.method_contract_currency'].search([]),
#         })

#     @http.route('/method_contract_currency/method_contract_currency/objects/<model("method_contract_currency.method_contract_currency"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('method_contract_currency.object', {
#             'object': obj
#         })