# Generated by Django 2.0.7 on 2019-03-24 08:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0001_initial'),
        ('warehouse', '0002_auto_20190324_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64, unique=True, verbose_name='Name')),
                ('phone', models.CharField(blank=True, max_length=10, verbose_name='Phone')),
                ('phone1', models.CharField(blank=True, max_length=10, verbose_name='Cell Phone')),
                ('date_started', models.DateField(default=django.utils.timezone.now, verbose_name='Date started')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='Balance')),
                ('vacation_days', models.IntegerField(default=0, verbose_name='Remaining Vacation Days')),
            ],
            options={
                'verbose_name': 'Υπάλληλος',
                'verbose_name_plural': '4. Employee',
            },
        ),
        migrations.RemoveField(
            model_name='person',
            name='occupation',
        ),
        migrations.AlterModelOptions(
            name='billcategory',
            options={'verbose_name_plural': '1. Manage Bill Category'},
        ),
        migrations.AlterModelOptions(
            name='billinvoice',
            options={'ordering': ['-date_expired'], 'verbose_name': 'Bill Invoice', 'verbose_name_plural': '2. Bill Invoice'},
        ),
        migrations.AlterModelOptions(
            name='occupation',
            options={'verbose_name': 'Occupation', 'verbose_name_plural': '3. Occupations'},
        ),
        migrations.RemoveField(
            model_name='payroll',
            name='person',
        ),
        migrations.AlterUniqueTogether(
            name='occupation',
            unique_together={('title', 'store')},
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.AddField(
            model_name='employee',
            name='occupation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='warehouse.Occupation', verbose_name='Occupation'),
        ),
        migrations.AddField(
            model_name='payroll',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='person_invoices', to='warehouse.Employee', verbose_name='Employee'),
            preserve_default=False,
        ),
    ]
