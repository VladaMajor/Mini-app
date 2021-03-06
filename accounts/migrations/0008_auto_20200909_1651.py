# Generated by Django 3.0.6 on 2020-09-09 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200909_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionaluserdata',
            name='creation_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='additionaluserdata',
            name='creator_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='additionaluserdata',
            name='last_update_timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='additionaluserdata',
            name='last_update_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='creation_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='creator_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='last_update_timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='last_update_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='m2m_device_sim',
            name='creation_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='m2m_device_sim',
            name='creator_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='m2m_device_sim',
            name='last_update_timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='m2m_device_sim',
            name='last_update_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='permission_type',
            name='creation_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='permission_type',
            name='creator_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='permission_type',
            name='last_update_timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='permission_type',
            name='last_update_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='permissions',
            name='creation_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='permissions',
            name='creator_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='permissions',
            name='last_update_timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='permissions',
            name='last_update_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sim',
            name='creation_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='sim',
            name='creator_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sim',
            name='last_update_timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='sim',
            name='last_update_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
