# Generated by Django 2.0.7 on 2019-04-02 12:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_sale', '0005_auto_20190402_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_expired',
            field=models.DateField(default=datetime.datetime(2019, 4, 2, 15, 18, 1, 536255), verbose_name='Date'),
        ),
    ]
