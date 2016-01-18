# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_paypal', '0002_invoice_invoiceitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='token',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
