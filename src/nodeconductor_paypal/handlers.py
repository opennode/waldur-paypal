import logging

from nodeconductor.logging import models as logging_models

from .log import event_logger
from . import models


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


def create_invoice(sender, invoice, issuer_details, **kwargs):
    """
    Creates an invoice when customer is "billed".
    :param sender: Invoice model
    :param invoice: Invoice instance
    :param issuer_details: details about issuer
    """
    paypal_invoice = models.Invoice.objects.create(customer=invoice.customer,
                                                   start_date=invoice.invoice_date,
                                                   end_date=invoice.due_date,
                                                   tax_percent=invoice.tax_percent,
                                                   issuer_details=issuer_details)

    for item in invoice.items:
        models.InvoiceItem.objects.create(
            invoice=paypal_invoice,
            price=item.price,
            tax=item.tax,
            quantity=item.usage_days * 24,
            unit_price=item.unit_price,
            unit_of_measure=models.InvoiceItem.UnitsOfMeasure.HOURS,
            name=item.name,
            start=item.start,
            end=item.end)
