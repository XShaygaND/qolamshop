# Generated by Django 5.0 on 2024-01-29 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_alter_order_address_alter_order_delivery_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='is_active',
            field=models.BooleanField(blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(blank=True, max_length=199),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CNC', 'Canceled'), ('LST', 'Lost'), ('REF', 'Refunded'), ('DMG', 'Damaged'), ('CRT', 'Created'), ('FIN', 'Delivered'), ('SNT', 'Sent to reeceiver')], default='Created', max_length=99),
        ),
    ]
