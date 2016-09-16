from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models import signals


class PayPalConfig(AppConfig):
    name = 'nodeconductor_paypal'
    verbose_name = 'PayPal'

    def ready(self):
        from . import handlers

        Invoice = self.get_model('Invoice')
        User = get_user_model()

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

        signals.post_save.connect(
            handlers.add_email_hooks_to_user,
            sender=User,
            dispatch_uid='nodeconductor_paypal.handlers.add_email_hooks_to_user',
        )
