import copy

from django.conf import settings
from django.test import override_settings


def override_paypal_settings(**kwargs):
    pp_settings = copy.deepcopy(settings.NODECONDUCTOR_PAYPAL)
    pp_settings.update(kwargs)
    return override_settings(NODECONDUCTOR_PAYPAL=pp_settings)
