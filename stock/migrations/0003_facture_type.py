# Generated by Django 5.0.4 on 2024-05-07 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_factureproduct_total_a'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='TYPE',
            field=models.CharField(choices=[('B', 'BON'), ('F', 'FACTURE')], default=2, max_length=1),
            preserve_default=False,
        ),
    ]
