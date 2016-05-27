# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 21:33
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0006_compensate_for_0003_bytestring_bug'),
        ('companies', '0002_auto_20160527_2133'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Journey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('departure_dt', models.DateTimeField(default=datetime.datetime.now, verbose_name='Start time')),
                ('arrival_dt', models.DateTimeField(verbose_name='End time')),
            ],
            options={
                'verbose_name': 'journey',
                'verbose_name_plural': 'List of journey',
            },
        ),
        migrations.CreateModel(
            name='LocationPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=150, verbose_name='Address')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.City', verbose_name='City')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'List of locations',
            },
        ),
        migrations.AddField(
            model_name='journey',
            name='arrival',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_point', to='courses.LocationPoint', verbose_name='Arrival'),
        ),
        migrations.AddField(
            model_name='journey',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Cars', verbose_name='Car'),
        ),
        migrations.AddField(
            model_name='journey',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.Country', verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='journey',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Customer'),
        ),
        migrations.AddField(
            model_name='journey',
            name='departure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_point', to='courses.LocationPoint', verbose_name='Departure'),
        ),
    ]
