# Generated by Django 4.2.1 on 2023-05-29 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlistapiapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishitems',
            old_name='quatity',
            new_name='quantity',
        ),
    ]