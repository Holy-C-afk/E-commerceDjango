# Generated by Django 5.1.5 on 2025-01-25 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_alter_cart_products_alter_cartitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='name',
            field=models.CharField(default=1, max_length=1),
            preserve_default=False,
        ),
    ]
