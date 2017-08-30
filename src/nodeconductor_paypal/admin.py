import logging

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from nodeconductor.core.tasks import send_task
from . import models

logger = logging.getLogger(__name__)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['customer', 'total_amount', 'start_date', 'end_date']
    actions = ['generate_invoice_pdf']

    def generate_invoice_pdf(self, request, queryset):
        for invoice in queryset.iterator():
            send_task('paypal', 'generate_invoice_pdf')(invoice.id)

        tasks_scheduled = queryset.count()
        message = _(
            'Scheduled generation of PDF for one invoice.',
            'Scheduled generation of PDF for %(tasks_scheduled)d invoice.',
            tasks_scheduled
        )
        message = message % {
            'tasks_scheduled': tasks_scheduled,
        }

        self.message_user(request, message)

    generate_invoice_pdf.short_description = "Generate invoice PDF"


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'amount', 'state', 'backend_id']

admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.Payment, PaymentAdmin)
