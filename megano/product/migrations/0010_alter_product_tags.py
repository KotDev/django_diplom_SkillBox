# Generated by Django 4.2.4 on 2023-08-21 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_delete_specifications'),
        ('product', '0009_alter_specifications_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(related_name='tags_product', to='shop.tag', verbose_name='Тэг'),
        ),
    ]
