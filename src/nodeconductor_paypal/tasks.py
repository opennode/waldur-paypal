import logging
from datetime import timedelta, datetime

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from nodeconductor.core import tasks as core_tasks
from nodeconductor.structure import SupportedServices
from .models import Invoice, Payment

logger = logging.getLogger(__name__)


class DebigCustomers(core_tasks.BackgroundTask):
    """ Fetch a list of shared services (services based on shared settings).
        Calculate the amount of consumed resources "yesterday" (make sure this task executed only once a day)
        Reduce customer's balance accordingly
        Stop online resource if needed
    """
    name = 'paypal.DebigCustomers'

    def is_equal(self, other_task, *args, **kwargs):
        return self.name == other_task.get('name')

    def run(self):
        date = datetime.now() - timedelta(days=1)
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1, microseconds=-1)

        # XXX: it's just a placeholder, it doesn't work properly now nor implemented anyhow
        #      perhaps it should merely use price estimates..

        models = SupportedServices.get_resource_models().values()

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
    # TODO [TM:8/30/17] remove in WAL-1119
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        logger.warning('Missing invoice with id %s', invoice.id)
        return

    invoice.generate_pdf()


class PaymentsCleanUp(core_tasks.BackgroundTask):
    name = 'paypal.PaymentsCleanUp'

    def is_equal(self, other_task, *args, **kwargs):
        return self.name == other_task.get('name')

    def run(self):
        timespan = settings.NODECONDUCTOR_PAYPAL.get('STALE_PAYMENTS_LIFETIME', timedelta(weeks=1))
        Payment.objects.filter(state=Payment.States.CREATED, created__lte=timezone.now() - timespan).delete()
