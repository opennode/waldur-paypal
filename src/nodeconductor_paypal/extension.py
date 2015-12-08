from __future__ import absolute_import

from nodeconductor.core import NodeConductorExtension


class PayPalExtension(NodeConductorExtension):

    class Settings:
        NODECONDUCTOR_PAYPAL = {
            'BACKEND': {
                'mode': 'sandbox',
                'client_id': '',
                'client_secret': '',
                'currency_name': 'USD',
                'return_url': 'http://example.com/payment/return',
            },
            'INVOICE': {
                'logo': 'robohare.png',
                'company': 'OpenNode',
                'bank': 'American Bank',
                'account': '123456789',
            }
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
                'task': 'nodeconductor.paypal.debit_customers',
                'schedule': crontab(hour=0, minute=30),
                'args': (),
            },
        }
