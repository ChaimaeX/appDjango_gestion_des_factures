# Generated by Django 3.2.1 on 2024-04-28 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0025_alter_facture_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]
