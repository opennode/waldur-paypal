from . import views


def register_in(router):
    router.register(r'paypal-payments', views.PaymentView, base_name='paypal-payment')
    router.register(r'paypal-invoices', views.InvoicesViewSet, base_name='paypal-invoice')
