# Generated by Django 3.1.4 on 2020-12-16 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='country',
            new_name='country_code',
        ),
    ]
