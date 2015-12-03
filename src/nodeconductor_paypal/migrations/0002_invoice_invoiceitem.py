# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0027_servicesettings_service_type'),
        ('nodeconductor_paypal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('total_amount', models.DecimalField(max_digits=9, decimal_places=2)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('pdf', models.FileField(null=True, upload_to=b'paypal-invoices', blank=True)),
                ('customer', models.ForeignKey(related_name='paypal_invoices', to='structure.Customer')),
            ],
            options={
                'ordering': ['-start_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=9, decimal_places=2)),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('backend_id', models.CharField(max_length=255, null=True, blank=True)),
                ('invoice', models.ForeignKey(related_name='items', to='nodeconductor_paypal.Invoice')),
            ],
            options={
                'ordering': ['invoice', '-created_at'],
            },
            bases=(models.Model,),
        ),
    ]
