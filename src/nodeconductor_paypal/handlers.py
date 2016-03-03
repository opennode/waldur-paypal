from .log import event_logger


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
