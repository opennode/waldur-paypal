from django.apps import AppConfig
from django.db.models import signals

from . import handlers


class PayPalConfig(AppConfig):
    name = 'nodeconductor_paypal'
    verbose_name = 'PayPal'

    def ready(self):
        Invoice = self.get_model('Invoice')

        signals.post_save.connect(
            handlers.log_invoice_save,
            sender=Invoice,
            dispatch_uid='nodeconductor_paypal.handlers.log_invoice_save',
        )

        signals.post_delete.connect(
            handlers.log_invoice_delete,
            sender=Invoice,
            dispatch_uid='nodeconductor_paypal.handlers.log_invoice_delete',
        )
