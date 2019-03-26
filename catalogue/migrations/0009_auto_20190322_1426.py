# Generated by Django 2.0.7 on 2019-03-22 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_auto_20190321_1311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productphotos',
            options={'ordering': ['-is_primary'], 'verbose_name_plural': 'Gallery'},
        ),
        migrations.AddField(
            model_name='attribute',
            name='class_related',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='catalogue.AttributeClass'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attribute',
            name='product_related',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='catalogue.Product', verbose_name='Προϊόν'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='catalogue.AttributeTitle'),
        ),
        migrations.AlterField(
            model_name='productcharacteristics',
            name='product_related',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='catalogue.Product'),
        ),
    ]
