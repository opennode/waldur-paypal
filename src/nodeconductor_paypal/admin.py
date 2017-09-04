import logging

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from nodeconductor.core.admin import ExecutorAdminAction
from nodeconductor.structure import admin as structure_admin

from . import models, executors

logger = logging.getLogger(__name__)


class InvoiceAdmin(structure_admin.BackendModelAdmin):
    list_display = ['customer', 'state', 'start_date', 'end_date', 'tax_percent', 'backend_id']
    actions = ['download_invoice_pdf', 'create_invoice']

    class CreateInvoice(ExecutorAdminAction):
        executor = executors.InvoiceCreateExecutor
        short_description = _('Create invoice')

    create_invoice = CreateInvoice()

    class DownloadInvoicePDF(ExecutorAdminAction):
        executor = executors.DownloadInvoicePDFExecutor
        short_description = _('Download invoice PDF')

    download_invoice_pdf = DownloadInvoicePDF()


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'amount', 'state', 'backend_id']

admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.Payment, PaymentAdmin)
