from rest_framework import serializers
from rest_framework.reverse import reverse

from nodeconductor.core import serializers as core_serializers

from .models import Payment, Invoice, InvoiceItem


class PaymentSerializer(core_serializers.AugmentedSerializerMixin,
                        serializers.HyperlinkedModelSerializer):

    amount = serializers.DecimalField(max_digits=9, decimal_places=2)
    state = serializers.ReadOnlyField(source='get_state_display')
    return_url = serializers.CharField(write_only=True)
    cancel_url = serializers.CharField(write_only=True)

    class Meta(object):
        model = Payment

        fields = (
            'url', 'uuid', 'created', 'modified', 'state',
            'amount', 'customer', 'return_url', 'cancel_url', 'approval_url', 'error_message'
        )

        read_only_fields = ('approval_url', 'error_message')
        protected_fields = ('customer', 'amount', 'return_url', 'cancel_url')

        extra_kwargs = {
            'url': {'lookup_field': 'uuid', 'view_name': 'paypal-payment-detail'},
            'customer': {'lookup_field': 'uuid', 'view_name': 'customer-detail'},
        }


class PaymentApproveSerializer(serializers.Serializer):
    payment_id = serializers.CharField()
    payer_id = serializers.CharField()
    token = serializers.CharField()


class PaymentCancelSerializer(serializers.Serializer):
    token = serializers.CharField()


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = InvoiceItem
        fields = ('amount', 'description', 'created_at')


class InvoiceSerializer(core_serializers.AugmentedSerializerMixin,
                        serializers.HyperlinkedModelSerializer):

    pdf = serializers.SerializerMethodField()
    items = InvoiceItemSerializer(many=True, read_only=True)

    class Meta(object):
        model = Invoice
        fields = (
            'url', 'uuid', 'total_amount', 'pdf',
            'start_date', 'end_date', 'items',
            'customer', 'customer_uuid', 'customer_name'
        )
        related_paths = ('customer',)
        extra_kwargs = {
            'url': {'lookup_field': 'uuid', 'view_name': 'paypal-invoice-detail'},
            'customer': {'lookup_field': 'uuid'}
        }

    def get_pdf(self, invoice):
        """
        Format URL to PDF view if file is specified
        """
        if invoice.pdf:
            return reverse('paypal-invoice-pdf',
                           kwargs={'uuid': invoice.uuid},
                           request=self.context['request'])
