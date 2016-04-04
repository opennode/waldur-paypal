import django_filters

from . import models


class PaymentFilter(django_filters.FilterSet):
    class Meta(object):
        model = models.Payment
        fields = ('customer',)

    customer = django_filters.CharFilter(
        name='customer__uuid',
        distinct=True,
    )


class InvoiceFilter(django_filters.FilterSet):
    class Meta(object):
        model = models.Invoice
        fields = ('customer',)

    customer = django_filters.CharFilter(
        name='customer__uuid',
        distinct=True,
    )

