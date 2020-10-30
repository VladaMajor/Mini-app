from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import randint

class AdditionalUserData(models.Model):
    status_types = (
        (1, "in_app"),
        (2, "in_chat"),
        (3, "in_background"),
        (4, "offline"),
    )
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    verified_email = models.BooleanField(default=False)
    street = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    home_number = models.CharField(max_length=200, null=True, blank=True)
    firebaseToken = models.TextField(null=True, blank=True)
    avatar = models.ImageField(blank=True, null=True, upload_to="avatars/%Y/%m", max_length=255, default="noimg.jpg")
    created_timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.IntegerField(choices=status_types, default=1)
    active_router = models.CharField(max_length=200, null=True, blank=True)
    notification = models.BooleanField(default=True)
    creator_id = models.IntegerField(null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_update_user_id = models.IntegerField(null=True, blank=True)
    last_update_timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Additional User Data"

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

@receiver(post_save, sender=User)
def create_user_additional_data(sender, instance, created, **kwargs):
    if created:
        AdditionalUserData.objects.create(user=instance)

class Device(models.Model):
    fk_account = models.ForeignKey(AdditionalUserData, on_delete=models.CASCADE, null=True)
    device_uuid = models.CharField(max_length=200, null=True, blank=True)
    mac_address = models.CharField(max_length=200, null=True, blank=True)
    vendor = models.CharField(max_length=200, null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    os = models.CharField(max_length=200, null=True, blank=True)
    creator_id = models.IntegerField(null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_update_user_id = models.IntegerField(null=True, blank=True)
    last_update_timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Device"

    def __str__(self):
        return self.fk_account.user.username

class Sim(models.Model):
    fk_account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    verified_sim_code = models.CharField(max_length=200, null=True, blank=True)
    creator_id = models.IntegerField(null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_update_user_id = models.IntegerField(null=True, blank=True)
    last_update_timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Sim"

    def __str__(self):
        return self.phone_number

class M2M_Device_Sim(models.Model):
    id_sim = models.ForeignKey('Sim', on_delete=models.CASCADE, null=True)
    id_device = models.ForeignKey('Device', on_delete=models.CASCADE, null=True)
    fk_account = models.IntegerField(null=True, blank=True)
    creator_id = models.IntegerField(null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_update_user_id = models.IntegerField(null=True, blank=True)
    last_update_timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "M2M Device Sim"

    def __str__(self):
        return self.id_device.fk_account.user.username

class Permissions(models.Model):
    table_name = models.CharField(max_length=200, null=True, blank=True)
    row_id = models.IntegerField(null=True, blank=True)
    fk_account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fk_account')
    fk_permission_type = models.ForeignKey(
        'Permission_type', on_delete=models.SET_NULL, null=True,
        blank=True, related_name='fk_permission_type', verbose_name="fk_permission_type")
    creator_id = models.IntegerField(null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_update_user_id = models.IntegerField(null=True, blank=True)
    last_update_timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Permissions"

    def __str__(self):
        return self.fk_account.username

class Permission_type(models.Model):
    perm = [
        ('Owner', 'Owner'),
        ('Edit', 'Edit'),
    ]
    name = models.CharField(max_length=10, choices=perm)
    creator_id = models.IntegerField(null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_update_user_id = models.IntegerField(null=True, blank=True)
    last_update_timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)    

    class Meta:
        verbose_name_plural = "Permission type"

    def __str__(self):
        return self.name
