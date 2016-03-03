import logging

from django.contrib import admin
from django.utils.translation import ungettext

from nodeconductor.core.tasks import send_task
from .models import Invoice, Payment

logger = logging.getLogger(__name__)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['customer', 'total_amount', 'start_date', 'end_date']
    actions = ['generate_invoice_pdf']

    def generate_invoice_pdf(self, request, queryset):
        for invoice in queryset.iterator():
            send_task('paypal', 'generate_invoice_pdf')(invoice.id)

        tasks_scheduled = queryset.count()
        message = ungettext(
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

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment, PaymentAdmin)
