# Generated by Django 4.2.6 on 2023-10-22 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SayfShop', '0012_alter_product_createddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='month',
            field=models.CharField(choices=[('sdsdsds', 'January'), ('hello', 'February')], default='hello', max_length=9),
        ),
    ]