from nodeconductor.logging.log import EventLogger, event_logger
from .models import Invoice, Payment


class InvoiceEventLogger(EventLogger):
    invoice = Invoice

    class Meta:
        event_types = ('invoice_deletion_succeeded',
                       'invoice_update_succeeded',
                       'invoice_creation_succeeded')


class PaymentEventLogger(EventLogger):
    payment = Payment

    class Meta:
        event_types = ('payment_creation_succeeded',
                       'payment_approval_succeeded',
                       'payment_cancel_succeeded')


event_logger.register('paypal_invoice', InvoiceEventLogger)
event_logger.register('paypal_payment', PaymentEventLogger)
