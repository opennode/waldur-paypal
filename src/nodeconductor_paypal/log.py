from nodeconductor.logging.log import EventLogger, event_logger
from .models import Payment


class PaymentEventLogger(EventLogger):
    payment = Payment

    class Meta:
        event_types = ('payment_creation_succeeded',
                       'payment_approval_succeeded',
                       'payment_cancel_succeeded')


event_logger.register('paypal_payment', PaymentEventLogger)
