# Generated by Django 4.2.6 on 2023-10-23 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SayfShop', '0014_remove_product_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('мобильные телефоны', 'мобильные телефоны'), ('телевизоры', 'телевизоры'), ('ноутбуки', 'ноутбуки'), ('компьютерные детали', 'компьютерные детали'), ('игровые приставки', 'игровые приставки'), ('наушники', 'наушники')], default='мобильные телефоны', max_length=30),
        ),
    ]
