import logging

from nodeconductor.logging import models as logging_models

from .log import event_logger
from . import models, helpers


logger = logging.getLogger(__name__)


def log_invoice_save(sender, instance, created=False, **kwargs):
    if created:
        event_logger.paypal_invoice.info(
            '{invoice_invoice_date}-{invoice_end_date}. Invoice for customer {customer_name} has been created.',
            event_type='invoice_creation_succeeded',
            event_context={
                'invoice': instance,
            })
    else:
        event_logger.paypal_invoice.info(
            '{invoice_invoice_date}-{invoice_end_date}. Invoice for customer {customer_name} has been updated.',
            event_type='invoice_update_succeeded',
            event_context={
                'invoice': instance,
            })


def log_invoice_delete(sender, instance, **kwargs):
    event_logger.paypal_invoice.info(
        '{invoice_invoice_date}-{invoice_end_date}. Invoice for customer {customer_name} has been deleted.',
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
    paypal_invoice = models.Invoice(
        customer=invoice.customer,
        year=invoice.year,
        month=invoice.month,
        invoice_date=invoice.invoice_date,
        end_date=invoice.due_date,
        tax_percent=invoice.tax_percent,
        issuer_details=issuer_details)

    if hasattr(invoice.customer, 'payment_details'):
        payment_details = invoice.customer.payment_details
        paypal_invoice.payment_details = {
            'company': payment_details.company,
            'address': payment_details.address,
            'country': payment_details.country,
            'email': payment_details.email,
            'postal': payment_details.postal,
            'phone': payment_details.phone,
            'bank': payment_details.bank,
        }

    paypal_invoice.save()

    for item in invoice.items:
        models.InvoiceItem.objects.create(
            invoice=paypal_invoice,
            price=item.price,
            tax=item.tax,
            quantity=helpers.get_invoice_item_quantity(item),
            unit_price=item.unit_price,
            unit_of_measure=helpers.convert_unit_of_measure(item.unit),
            name=item.name,
            start=item.start,
            end=item.end)
