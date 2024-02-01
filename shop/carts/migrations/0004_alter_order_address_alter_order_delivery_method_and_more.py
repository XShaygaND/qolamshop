# Generated by Django 5.0 on 2024-01-29 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_order_address_order_phone_order_postal_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(default=None, max_length=199),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_method',
            field=models.CharField(choices=[('SDD', 'Same day delivery'), ('FD', 'Fast delivery'), ('ND', 'Normal delivery')], default='Normal delivery', max_length=99),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(default=None, max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='postal_code',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('SNT', 'Sent to reeceiver'), ('CNC', 'Canceled'), ('LST', 'Lost'), ('FIN', 'Delivered'), ('REF', 'Refunded'), ('CRT', 'Created'), ('DMG', 'Damaged')], default='Created', max_length=99),
        ),
    ]