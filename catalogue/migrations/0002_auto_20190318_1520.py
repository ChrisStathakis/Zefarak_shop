# Generated by Django 2.1.7 on 2019-03-18 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Ποσότητα')),
                ('order_discount', models.IntegerField(blank=True, default=0, null=True, verbose_name="'Εκπτωση Τιμολογίου σε %")),
                ('price_buy', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Τιμή Αγοράς')),
            ],
            options={
                'verbose_name_plural': '2. Μεγεθολόγιο',
                'ordering': ['title'],
            },
            managers=[
                ('my_query', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='AttributeTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('ordering_by', models.IntegerField(default=0, help_text='Bigger is first')),
            ],
            options={
                'ordering': ['ordering_by'],
            },
        ),
        migrations.CreateModel(
            name='Characteristics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Κατάσταση')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('costum_ordering', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=120, unique=True)),
                ('user_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CharacteristicsValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Κατάσταση')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('costum_ordering', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=120, unique=True)),
                ('user_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCharacteristics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ProductClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('is_service', models.BooleanField(default=False, verbose_name='Is service')),
                ('have_transcations', models.BooleanField(default=True, verbose_name='Will use transcations?')),
                ('have_attribute', models.BooleanField(default=False, verbose_name='Have attributes?')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='have_transcations',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_service',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='productcharacteristics',
            name='product_related',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='catalogue.Product'),
        ),
        migrations.AddField(
            model_name='productcharacteristics',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Characteristics'),
        ),
        migrations.AddField(
            model_name='productcharacteristics',
            name='value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.CharacteristicsValue'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='product_related',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_sizes', to='catalogue.Product', verbose_name='Προϊόν'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='catalogue.AttributeTitle', verbose_name='Νούμερο'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='catalogue.ProductClass'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='productcharacteristics',
            unique_together={('product_related', 'title')},
        ),
        migrations.AlterUniqueTogether(
            name='attribute',
            unique_together={('title', 'product_related')},
        ),
    ]
