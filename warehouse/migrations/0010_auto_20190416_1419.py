# Generated by Django 2.0 on 2019-04-16 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0009_auto_20190414_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='taxes_modifier',
            field=models.CharField(choices=[('1', 13), ('2', 23), ('3', 24), ('4', 0)], default='1', max_length=1),
        ),
    ]