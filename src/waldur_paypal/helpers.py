import copy

from django.conf import settings
from django.test import override_settings

from . import models


def override_paypal_settings(**kwargs):
    plugin_settings = copy.deepcopy(settings.WALDUR_PAYPAL)
    plugin_settings.update(kwargs)
    return override_settings(WALDUR_PAYPAL=plugin_settings)


def convert_unit_of_measure(unit):
    if unit.lower() == 'quantity':
        return models.InvoiceItem.UnitsOfMeasure.QUANTITY
    else:
        return models.InvoiceItem.UnitsOfMeasure.HOURS


def get_invoice_item_quantity(item):
    unit_of_measure = convert_unit_of_measure(item.unit)
    if unit_of_measure == models.InvoiceItem.UnitsOfMeasure.HOURS:
        return item.usage_days * 24
    else:
        return item.quantity
