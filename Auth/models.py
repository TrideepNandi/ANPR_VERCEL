from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('hod', 'HOD'),
        ('director', 'Director'),
        ('management', 'Management'),
        ('operator', 'Operator'),
        ('user', 'User'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='user')
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name="customuser_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_user_permissions")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.username = self.email  # Set username to the email address.
        super().save(*args, **kwargs)  # Call the "real" save() method.

        group, created = Group.objects.get_or_create(name=self.user_type)  # Create group if it doesn't exist already.

        if created:
            # Set permissions for the group here.
            pass

        self.groups.add(group)  # Add the user to the group.
