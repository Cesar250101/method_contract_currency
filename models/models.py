# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class Contratos(models.Model):
    _inherit = 'contract.contract'

    @api.multi
    def recurring_create_invoice(self):
        invoice=super(Contratos, self).recurring_create_invoice()
        if  self.pricelist_id.currency_id.name=='UF':
            if self.pricelist_id.currency_id.rate==0:
                raise UserError(u'Tasa de cambio para UF no existe!')
            tasa=self.pricelist_id.currency_id.rate
            factura=self.env['account.invoice'].search([('id','=',invoice.id)])
            if factura:
                factura.amount_untaxed_invoice_signed=factura.amount_untaxed_invoice_signed/tasa
                factura.amount_tax_signed=factura.amount_tax_signed/tasa
                factura.amount_tax=factura.amount_tax/tasa
                factura.amount_total_signed=factura.amount_total_signed/tasa
                factura.amount_total=factura.amount_total/tasa
                factura.amount_untaxed=factura.amount_untaxed/tasa
                factura.residual=factura.amount_total
                factura.residual_signed=factura.amount_total

            factura_lineas=self.env['account.invoice.line'].search([('invoice_id','=',invoice.id)])
            if factura_lineas:
                for fl in factura_lineas:
                    fl.price_unit=fl.price_unit/tasa
                    
            factura_tax=self.env['account.invoice.tax'].search([('invoice_id','=',invoice.id)])
            if factura_tax:
                for ft in factura_tax:
                    ft.amount=ft.amount/tasa

        comprobante = self.env['account.move'].search([('id', '=', factura.move_id.id)])
        for c in comprobante:
            c.state='draft'
        comprobante_lineas=self.env['account.move.line'].search([('move_id','=',factura.move_id.id)])
        for cl in comprobante_lineas:
            debito=cl.debit/tasa
            credito=cl.credit/tasa
            balance=cl.balance/tasa
            if cl.amount_residual!=0:
                residual=cl.amount_residual/tasa
                self.env.cr.execute("UPDATE account_move_line set debit=%s, credit=%s, amount_residual=%s, balance=%s  WHERE move_id = %s AND id=%s",
                                    (debito, credito,residual,balance, cl.move_id.id, cl.id))
            else:
                self.env.cr.execute("UPDATE account_move_line set debit=%s, credit=%s, balance=%s  WHERE move_id = %s AND id=%s",
                                    (debito, credito,balance, cl.move_id.id, cl.id))
        factura_id=factura.id
        self.env.cr.execute("UPDATE account_invoice set residual=amount_total,residual_signed=amount_total,residual_company_signed=amount_total  WHERE id = %s",
                (factura_id,))

        for c in comprobante:
            c.state='posted'
        factura._compute_residual()







