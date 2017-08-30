import factory

from django.core.urlresolvers import reverse

from nodeconductor.structure.tests import factories as structure_factories

from nodeconductor_paypal import models


class PaypalPaymentFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = models.Payment

    amount = 10
    customer = factory.SubFactory(structure_factories.CustomerFactory)
    backend_id = factory.Sequence(lambda n: 'PAYMENT-ABC-%s' % n)
    token = factory.Sequence(lambda n: 'TOKEN-%s' % n)

    @classmethod
    def get_url(self, payment=None, action=None):
        if payment is None:
            payment = PaypalPaymentFactory()
        url = 'http://testserver' + reverse('paypal-payment-detail', kwargs={'uuid': payment.uuid})
        return url if action is None else url + action + '/'

    @classmethod
    def get_list_url(cls):
        return 'http://testserver' + reverse('paypal-payment-list')
