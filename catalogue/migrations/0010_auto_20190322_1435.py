# Generated by Django 2.0.7 on 2019-03-22 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0009_auto_20190322_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeProductClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.AttributeClass')),
                ('product_related', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attr_class', to='catalogue.Product', verbose_name='Προϊόν')),
            ],
        ),
        migrations.AlterField(
            model_name='attribute',
            name='class_related',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.AttributeProductClass'),
        ),
        migrations.AlterUniqueTogether(
            name='attributeproductclass',
            unique_together={('class_related', 'product_related')},
        ),
    ]
