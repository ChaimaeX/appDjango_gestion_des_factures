# Generated by Django 4.2.1 on 2024-04-03 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='facture',
        ),
        migrations.AddField(
            model_name='facture',
            name='produit',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to='stock.produit'),
            preserve_default=False,
        ),
    ]