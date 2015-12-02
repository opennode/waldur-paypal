import logging

from django.conf import settings
from django.shortcuts import redirect
from django.views.static import serve
from django_fsm import TransitionNotAllowed

from rest_framework import mixins, viewsets, permissions, decorators, exceptions
from rest_framework.reverse import reverse

from nodeconductor.structure.filters import GenericRoleFilter
from nodeconductor.structure.models import CustomerRole

from .backend import PaypalBackend, PayPalError
from .log import event_logger
from .models import Payment, Invoice, InvoiceItem
from .serializers import PaymentSerializer, PaymentApproveSerializer, InvoiceSerializer


class CreateByStaffOrOwnerMixin(object):

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = serializer.validated_data['customer']

        if not self.request.user.is_staff and not customer.has_user(self.request.user, CustomerRole.OWNER):
            raise exceptions.PermissionDenied()
        return super(CreateByStaffOrOwnerMixin, self).create(request)


class PaymentView(CreateByStaffOrOwnerMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'uuid'
    filter_backends = (GenericRoleFilter,)
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.DjangoObjectPermissions,
    )

    def perform_create(self, serializer):
        """
        Create new payment via Paypal gateway
        """

        customer = serializer.validated_data['customer']
        payment = serializer.save()
        url = reverse('paypal-payment-detail', kwargs={'uuid': payment.uuid.hex}, request=self.request)

        try:
            backend = PaypalBackend()
            backend_payment = backend.make_payment(
                amount=serializer.validated_data['amount'],
                description='Replenish account in NodeConductor for %s' % customer.name,
                return_url=url + 'approve/',
                cancel_url=url + 'cancel/')

            payment.backend_id = backend_payment.payment_id
            payment.approval_url = backend_payment.approval_url
            payment.set_created()
            payment.save()

            event_logger.paypal_payment.info(
                'Created new payment for {customer_name}',
                event_type='payment_creation_succeeded',
                event_context={'payment': payment}
            )

        except PayPalError as e:
            logging.warning('Unable to create payment because of backend error %s', e)
            payment.set_erred()
            payment.save()
            raise exceptions.APIException()

    @decorators.detail_route()
    def approve(self, request, uuid):
        """
        Callback view for Paypal payment approval.
        Do not use it directly. It is internal API.
        """
        payment = self.get_object()

        serializer = PaymentApproveSerializer(instance=payment, data={
            'payment_id': request.query_params.get('paymentId'),
            'payer_id': request.query_params.get('PayerID')
        })
        serializer.is_valid(raise_exception=True)

        payment_id = serializer.validated_data['payment_id']
        payer_id = serializer.validated_data['payer_id']

        try:
            backend = PaypalBackend()
            backend.approve_payment(payment_id, payer_id)

            payment.customer.credit_account(payment.amount)
            payment.set_approved()
            payment.save()

            event_logger.paypal_payment.info(
                'Payment for {customer_name} has been approved',
                event_type='payment_approval_succeeded',
                event_context={'payment': payment}
            )
            return redirect(backend.return_url)

        # Do not raise error
        except PayPalError as e:
            logging.warning('Unable to approve payment because of backend error %s', e)
            payment.set_erred()
            payment.save()
            return redirect(backend.return_url)

        except TransitionNotAllowed:
            logging.warning('Unable to approve payment because of invalid state')
            payment.set_erred()
            payment.save()
            return redirect(backend.return_url)

    @decorators.detail_route()
    def cancel(self, request, uuid):
        """
        Callback view for Paypal payment cancel.
        Do not use it directly. It is internal API.
        """
        payment = self.get_object()
        backend = PaypalBackend()
        try:
            payment.set_cancelled()
            payment.save()

            event_logger.paypal_payment.info(
                'Payment for {customer_name} has been cancelled',
                event_type='payment_cancel_succeeded',
                event_context={'payment': payment}
            )
            return redirect(backend.return_url)

        # Do not raise error
        except TransitionNotAllowed:
            logging.warning('Unable to cancel payment because of invalid state')
            return redirect(backend.return_url)


class InvoicesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'uuid'

    def _serve_pdf(self, request, pdf):
        if not pdf:
            raise exceptions.NotFound("There's no PDF for this invoice")

        response = serve(request, pdf.name, document_root=settings.MEDIA_ROOT)
        if request.query_params.get('download'):
            filename = pdf.name.split('/')[-1]
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

        return response

    @decorators.detail_route()
    def pdf(self, request, uuid=None):
        return self._serve_pdf(request, self.get_object().pdf)
