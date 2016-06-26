# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_paypal', '0004_payment_error_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='total_amount',
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='tax',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=2),
        ),
        migrations.AddField(
            model_name='payment',
            name='tax',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=2),
        ),
    ]
