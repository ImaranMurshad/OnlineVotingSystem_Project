from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('host', 'Election Host'),
        ('voter', 'Voter'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    mobile = models.CharField(max_length=15, null=True, blank=True)

    status = models.IntegerField(default=0)  # 0=pending
    created_date = models.DateTimeField(auto_now_add=True)

    host = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)