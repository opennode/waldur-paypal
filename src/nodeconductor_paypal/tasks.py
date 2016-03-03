import logging
from datetime import timedelta, datetime

from celery import shared_task

from nodeconductor.structure import SupportedServices
from .models import Invoice

logger = logging.getLogger(__name__)


@shared_task(name='nodeconductor.paypal.debit_customers')
def debit_customers():
    """ Fetch a list of shared services (services based on shared settings).
        Calculate the amount of consumed resources "yesterday" (make sure this task executed only once a day)
        Reduce customer's balance accordingly
        Stop online resource if needed
    """

    date = datetime.now() - timedelta(days=1)
    start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=1, microseconds=-1)

    # XXX: it's just a placeholder, it doesn't work properly now nor implemented anyhow
    #      perhaps it should merely use price estimates..

    # TODO: remove once iaas has been deprecated
    from nodeconductor.iaas.models import Instance
    models = filter(lambda model: model != Instance, SupportedServices.get_resource_models().values())

    for model in models:
        resources = model.objects.filter(
            service_project_link__service__settings__shared=True)

        for resource in resources:
            try:
                data = resource.get_cost(start_date, end_date)
            except NotImplementedError:
                continue
            else:
                resource.customer.debit_account(data['total_amount'])


@shared_task(name='nodeconductor.paypal.generate_invoice_pdf')
def generate_invoice_pdf(invoice_id):
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        logger.warning('Missing invoice with id %s', invoice.id)
        return

    invoice.generate_pdf()
