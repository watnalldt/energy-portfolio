# Generated by Django 4.2.5 on 2023-09-12 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0004_alter_contract_is_directors_approval_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='supplier_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Supplier Start Date'),
        ),
        migrations.AddField(
            model_name='historicalcontract',
            name='supplier_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Supplier Start Date'),
        ),
    ]
