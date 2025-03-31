from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  
        blank=True
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)


# Role Model for RBAC
class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


# Address Model for Multiple Addresses
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)


# Token Blacklist for Logout
class TokenBlacklist(models.Model):
    token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
