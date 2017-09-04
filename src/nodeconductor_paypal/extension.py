from __future__ import absolute_import

from datetime import timedelta

from nodeconductor.core import NodeConductorExtension


class PayPalExtension(NodeConductorExtension):

    class Settings(object):
        NODECONDUCTOR_PAYPAL = {
            'ENABLED': False,
            'BACKEND': {
                'mode': 'sandbox',
                'client_id': '',
                'client_secret': '',
                'currency_name': 'USD',
            },
            'INVOICE': {
                'template': 'https://www.sandbox.paypal.com/invoice/payerView/details/%(invoice_id)s?printPdfMode=true',
            },
            'STALE_PAYMENTS_LIFETIME': timedelta(weeks=1)
        }

    @staticmethod
    def django_app():
        return 'nodeconductor_paypal'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in

    @staticmethod
    def celery_tasks():
        from celery.schedules import crontab
        return {
            'debit-customers': {
                'task': 'paypal.DebigCustomers',
                'schedule': crontab(hour=0, minute=30),
                'args': (),
            },
            'payments-cleanup': {
                'task': 'paypal.PaymentsCleanUp',
                'schedule': timedelta(hours=24),
                'args': (),
            },
            'send-invoices': {
                'task': 'paypal.SendInvoices',
                'schedule': timedelta(hours=24),
                'args': (),
            }
        }
