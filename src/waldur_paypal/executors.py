from celery import chain

from nodeconductor.core import executors as core_executors, tasks as core_tasks


class DownloadInvoicePDFExecutor(core_executors.BaseExecutor):

    @classmethod
    def get_task_signature(cls, invoice, serialized_invoice, **kwargs):
        return core_tasks.BackendMethodTask().si(serialized_invoice, 'download_invoice_pdf')


class InvoiceCreateExecutor(core_executors.BaseExecutor):

    @classmethod
    def get_task_signature(cls, invoice, serialized_invoice, **kwargs):
        tasks = [
            core_tasks.BackendMethodTask().si(serialized_invoice, 'create_invoice'),
            core_tasks.BackendMethodTask().si(serialized_invoice, 'download_invoice_pdf'),
        ]

        return chain(*tasks)
