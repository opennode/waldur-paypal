from __future__ import unicode_literals

from datetime import timedelta
from random import randint
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from nodeconductor.structure.models import Customer
from ...models import Invoice, InvoiceItem


class Command(BaseCommand):
    args = '<customer_id>'
    help = 'Creates sample invoices'

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('Customer ID is not specified.')

        try:
            customer = Customer.objects.get(id=args[0])
        except Customer.DoesNotExist:
            raise CommandError('Customer is not found.')

        for invoice_index in range(1, 6):
            start_date = timezone.now() - timedelta(days=invoice_index * 30)
            end_date = start_date + timedelta(days=30)
            amount = randint(10, 100)

            invoice = Invoice.objects.create(
                customer=customer,
                start_date=start_date,
                end_date=end_date,
                total_amount=amount)

            InvoiceItem.objects.create(
                invoice=invoice,
                description='Monthly fee for premium plan',
                amount=amount,
                tax=amount/10.0,
                created_at=start_date)
