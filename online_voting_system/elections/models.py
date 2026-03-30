from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Election(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title