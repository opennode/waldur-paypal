# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_paypal', '0003_payment_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='error_message',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
