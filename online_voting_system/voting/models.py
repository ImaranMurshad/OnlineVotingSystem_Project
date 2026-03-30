from django.db import models
from django.conf import settings
from elections.models import Election

User = settings.AUTH_USER_MODEL


# =========================
# 🔹 CANDIDATE MODEL
# =========================
class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# =========================
# 🔹 VOTE MODEL
# =========================
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')

    class Meta:
        unique_together = ('user', 'election')  # 🔥 prevents duplicate votes

    def __str__(self):
        return f"{self.user} voted in {self.election}"