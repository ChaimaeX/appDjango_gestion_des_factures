# Generated by Django 5.0.4 on 2024-04-17 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_factureproduct_quantity_achat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='category',
            field=models.TextField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]