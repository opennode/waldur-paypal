import logging

from django.conf import settings
from django.views.static import serve
from django_fsm import TransitionNotAllowed

from rest_framework import mixins, viewsets, permissions, decorators, exceptions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from nodeconductor.structure.filters import GenericRoleFilter
from nodeconductor.structure.models import CustomerRole

from .backend import PaypalBackend, PayPalError
from .log import event_logger
from .models import Payment, Invoice
from .serializers import PaymentSerializer, PaymentApproveSerializer, InvoiceSerializer, PaymentCancelSerializer


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

        return_url = serializer.validated_data.pop('return_url')
        cancel_url = serializer.validated_data.pop('cancel_url')

        customer = serializer.validated_data['customer']
        payment = serializer.save()

        try:
            backend_payment = PaypalBackend().make_payment(
                amount=serializer.validated_data['amount'],
                description='Replenish account in NodeConductor for %s' % customer.name,
                return_url=return_url,
                cancel_url=cancel_url)

            payment.backend_id = backend_payment.payment_id
            payment.approval_url = backend_payment.approval_url
            payment.token = backend_payment.token
            payment.set_created()
            payment.save()

            serializer.instance = payment

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

    def get_payment(self, token):
        """
        Find Paypal payment object in the database by token
        and check if current user has access to it.
        :param token: string
        :return: Payment object
        """
        error_message = "Payment with token %s does not exist" % token

        try:
            payment = Payment.objects.get(token=token)
        except Payment.DoesNotExist:
            raise NotFound(error_message)

        is_owner = payment.customer.has_user(self.request.user, CustomerRole.OWNER)
        if not self.request.user.is_staff and not is_owner:
            raise NotFound(error_message)

        return payment

    @decorators.list_route(methods=['POST'])
    def approve(self, request):
        """
        Approve Paypal payment.
        """
        serializer = PaymentApproveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment_id = serializer.validated_data['payment_id']
        payer_id = serializer.validated_data['payer_id']
        token = serializer.validated_data['token']
        payment = self.get_payment(token)

        try:
            PaypalBackend().approve_payment(payment_id, payer_id)

            payment.customer.credit_account(payment.amount)
            payment.set_approved()
            payment.save()

            event_logger.paypal_payment.info(
                'Payment for {customer_name} has been approved.',
                event_type='payment_approval_succeeded',
                event_context={'payment': payment}
            )
            return Response({'detail': 'Payment has been approved.'}, status=status.HTTP_200_OK)

        except PayPalError as e:
            message = 'Unable to approve payment because of backend error %s' % e
            logging.warning(message)
            payment.save()
            raise exceptions.APIException(message)

        except TransitionNotAllowed:
            payment.set_erred()
            payment.save()
            return Response({'detail': 'Unable to approve payment because of invalid state.'},
                            status=status.HTTP_409_CONFLICT)

    @decorators.list_route(methods=['POST'])
    def cancel(self, request):
        """
        Cancel Paypal payment.
        """
        serializer = PaymentCancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        payment = self.get_payment(token)

        try:
            payment.set_cancelled()
            payment.save()

            event_logger.paypal_payment.info(
                'Payment for {customer_name} has been cancelled.',
                event_type='payment_cancel_succeeded',
                event_context={'payment': payment}
            )
            return Response({'detail': 'Payment has been cancelled.'}, status=status.HTTP_200_OK)

        except TransitionNotAllowed:
            return Response({'detail': 'Unable to cancel payment because of invalid state.'},
                            status=status.HTTP_409_CONFLICT)


class InvoicesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'uuid'

    def _serve_pdf(self, request, pdf):
        if not pdf:
            raise exceptions.NotFound("There's no PDF for this invoice.")

        response = serve(request, pdf.name, document_root=settings.MEDIA_ROOT)
        if request.query_params.get('download'):
            filename = pdf.name.split('/')[-1]
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

        return response

    @decorators.detail_route()
    def pdf(self, request, uuid=None):
        return self._serve_pdf(request, self.get_object().pdf)
