# Generated by Django 5.0.4 on 2024-04-24 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0009_alter_facture_facture_date_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facture',
            name='comments',
        ),
    ]