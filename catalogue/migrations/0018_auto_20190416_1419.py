# Generated by Django 2.0 on 2019-04-16 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0006_auto_20190402_1611'),
        ('catalogue', '0017_auto_20190414_1013'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorPaycheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=150)),
                ('date_expired', models.DateField()),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('is_paid', models.BooleanField(default=False)),
                ('payment_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='site_settings.PaymentMethod')),
            ],
        ),
        migrations.AlterField(
            model_name='vendor',
            name='address',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='city',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Detaiks'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Cellphone'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone1',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='title',
            field=models.CharField(max_length=70, unique=True, verbose_name="'Title"),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vat_city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Vat City'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='zipcode',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Zipcode'),
        ),
        migrations.AddField(
            model_name='vendorpaycheck',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogue.Vendor'),
        ),
    ]