# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-20 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_01', models.DecimalField(decimal_places=5, default=0.0, max_digits=8)),
                ('term_02', models.DecimalField(decimal_places=5, default=0.0, max_digits=8)),
                ('term_03', models.DecimalField(decimal_places=5, default=0.0, max_digits=8)),
                ('term_04', models.DecimalField(decimal_places=5, default=0.0, max_digits=8)),
                ('term_05', models.DecimalField(decimal_places=5, default=0.0, max_digits=8)),
                ('water_sensor', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
