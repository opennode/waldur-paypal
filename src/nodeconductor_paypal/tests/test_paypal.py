import decimal
import mock

from rest_framework import test, status

from nodeconductor.structure import models as structure_models
from nodeconductor.structure.tests import factories as structure_factories
from nodeconductor_paypal.backend import PaypalPayment, PayPalError
from nodeconductor_paypal.models import Payment

from .factories import PaypalPaymentFactory


class BasePaymentTest(test.APISimpleTestCase):

    def setUp(self):
        self.customer = structure_factories.CustomerFactory(balance=0)
        self.owner = structure_factories.UserFactory()
        self.other = structure_factories.UserFactory()
        self.staff = structure_factories.UserFactory(is_staff=True)
        self.customer.add_user(self.owner, structure_models.CustomerRole.OWNER)

        self.valid_request = {
            'amount': decimal.Decimal('9.99'),
            'customer': structure_factories.CustomerFactory.get_url(self.customer),
            'return_url': 'http://example.com/return/',
            'cancel_url': 'http://example.com/cancel/'
        }

        self.valid_response = {
            'approval_url': 'https://www.paypal.com/webscr?cmd=_express-checkout&token=EC-60U79048BN7719609',
            'payer_id': '7E7MGXCWTTKK2',
            'token': 'EC-60U79048BN7719609'
        }


class PaymentCreationTest(BasePaymentTest):

    def create_payment(self, user, fail=False):
        with mock.patch('nodeconductor_paypal.views.PaypalBackend') as backend:
            if fail:
                backend().make_payment.side_effect = PayPalError()
            else:
                backend().make_payment.return_value = PaypalPayment(
                        payment_id='PAY-6RV70583SB702805EKEYSZ6Y',
                        approval_url=self.valid_response['approval_url'],
                        token=self.valid_response['token'])

            self.client.force_authenticate(user)
            return self.client.post(PaypalPaymentFactory.get_list_url(), data=self.valid_request)

    # Positive tests

    def test_staff_can_create_payment_for_any_customer(self):
        response = self.create_payment(self.staff)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(self.valid_response['approval_url'], response.data['approval_url'])

    def test_user_can_create_payment_for_owned_customer(self):
        response = self.create_payment(self.owner)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    # Negative tests

    def test_user_can_not_create_payment_for_other_customer(self):
        response = self.create_payment(self.other)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_when_backend_fails_error_returned(self):
        response = self.create_payment(self.owner, fail=True)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentApprovalTest(BasePaymentTest):

    def approve_payment(self, user, amount=None, fail=False):
        payment = PaypalPaymentFactory(customer=self.customer,
                                       state=Payment.States.CREATED,
                                       amount=amount or 100.0)

        with mock.patch('nodeconductor_paypal.views.PaypalBackend') as backend:
            if fail:
                backend().approve_payment.side_effect = PayPalError()

            self.client.force_authenticate(user)
            return self.client.post(PaypalPaymentFactory.get_list_url() + 'approve/', data={
                'payment_id': payment.backend_id,
                'payer_id': self.valid_response['payer_id'],
                'token': payment.token
            })

    # Positive tests

    def test_staff_can_approve_any_payment(self):
        response = self.approve_payment(self.staff)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_user_can_approve_payment_for_owned_customer(self):
        response = self.approve_payment(self.owner)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_if_payment_approved_balance_is_increased(self):
        self.approve_payment(self.owner, 10.0)
        customer = structure_models.Customer.objects.get(id=self.customer.id)
        self.assertEqual(customer.balance, self.customer.balance + 10.0)

    # Negative tests

    def test_user_can_not_approve_payment_for_other_customer(self):
        response = self.approve_payment(self.other)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_if_backend_fails_balance_is_not_increased(self):
        response = self.approve_payment(self.owner, fail=True)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        customer = structure_models.Customer.objects.get(id=self.customer.id)
        self.assertEqual(customer.balance, self.customer.balance)


class PaymentCancellationTest(BasePaymentTest):

    def cancel_payment(self, user):
        self.client.force_authenticate(user)
        payment = PaypalPaymentFactory(customer=self.customer, state=Payment.States.CREATED)
        return self.client.post(PaypalPaymentFactory.get_list_url() + 'cancel/', data={
            'token': payment.token
        })

    # Positive tests

    def test_staff_can_cancel_any_payment(self):
        response = self.cancel_payment(self.staff)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_user_can_cancel_payment_for_owned_customer(self):
        response = self.cancel_payment(self.owner)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Negative test

    def test_user_can_not_cancel_payment_for_other_customer(self):
        response = self.cancel_payment(self.other)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
