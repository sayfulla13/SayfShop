# Generated by Django 4.2.6 on 2023-10-22 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SayfShop', '0003_remove_product_date_alter_product_createddate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='img',
        ),
    ]
