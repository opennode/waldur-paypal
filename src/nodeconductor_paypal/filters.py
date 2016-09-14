import django_filters

from nodeconductor.core.filters import UUIDFilter
from . import models


class PaymentFilter(django_filters.FilterSet):
    class Meta(object):
        model = models.Payment
        fields = ('customer',)

    customer = UUIDFilter(
        name='customer__uuid',
        distinct=True,
    )


class InvoiceFilter(django_filters.FilterSet):
    class Meta(object):
        model = models.Invoice
        fields = ('customer',)

    customer = UUIDFilter(
        name='customer__uuid',
        distinct=True,
    )

