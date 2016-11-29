import logging

from nodeconductor.logging import models as logging_models

from .log import event_logger


logger = logging.getLogger(__name__)


def log_invoice_save(sender, instance, created=False, **kwargs):
    if created:
        event_logger.paypal_invoice.info(
            '{invoice_start_date}-{invoice_end_date}. Invoice for customer {customer_name} has been created.',
            event_type='invoice_creation_succeeded',
            event_context={
                'invoice': instance,
            })
    else:
        event_logger.paypal_invoice.info(
            '{invoice_start_date}-{invoice_end_date}. Invoice for customer {customer_name} has been updated.',
            event_type='invoice_update_succeeded',
            event_context={
                'invoice': instance,
            })


def log_invoice_delete(sender, instance, **kwargs):
    event_logger.paypal_invoice.info(
        '{invoice_start_date}-{invoice_end_date}. Invoice for customer {customer_name} has been deleted.',
        event_type='invoice_deletion_succeeded',
        event_context={
            'invoice': instance,
        })


def add_email_hooks_to_user(sender, instance, created, **kwargs):
    if not created:
        return
    event_types = ['invoice_creation_succeeded', 'payment_creation_succeeded',
                   'payment_approval_succeeded', 'payment_cancel_succeeded']
    user = instance
    if not user.email:
        logger.warn('Cannot add default email hooks to user %s (PK: %s). He does not have email.', user, user.pk)

    logging_models.EmailHook.objects.create(
        user=user,
        event_types=event_types,
        email=user.email,
    )
