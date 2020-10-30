# Generated by Django 3.0.6 on 2020-09-09 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200909_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionaluserdata',
            name='creation_timestamp',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='additionaluserdata',
            name='last_update_timestamp',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='creation_timestamp',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_update_timestamp',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]