# Generated by Django 3.0.6 on 2020-10-22 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20201019_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sim',
            name='iccid',
        ),
    ]
