from rest_framework import serializers

from nodeconductor.core import serializers as core_serializers

from .models import Payment, Invoice, InvoiceItem


class PaymentSerializer(core_serializers.AugmentedSerializerMixin,
                        serializers.HyperlinkedModelSerializer):

    amount = serializers.DecimalField(max_digits=9, decimal_places=2)
    state = serializers.ReadOnlyField(source='get_state_display')

    class Meta(object):
        model = Payment

        fields = (
            'url', 'uuid', 'created', 'modified', 'state',
            'amount', 'customer', 'approval_url'
        )

        read_only_fields = ('approval_url',)
        protected_fields = ('customer', 'amount')

        extra_kwargs = {
            'url': {'lookup_field': 'uuid', 'view_name': 'paypal-payment-detail'},
            'customer': {'lookup_field': 'uuid', 'view_name': 'customer-detail'},
        }


class PaymentApproveSerializer(serializers.Serializer):
    payment_id = serializers.CharField()
    payer_id = serializers.CharField()

    def validate(self, validated_data):
        if self.instance.backend_id != validated_data['payment_id']:
            raise serializers.ValidationError('Invalid paymentId')
        return validated_data


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = InvoiceItem
        fields = ('amount', 'description', 'created_at')


class InvoiceSerializer(core_serializers.AugmentedSerializerMixin,
                        serializers.HyperlinkedModelSerializer):

    pdf = serializers.HyperlinkedIdentityField(view_name='paypal-invoice-pdf', lookup_field='uuid')
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
