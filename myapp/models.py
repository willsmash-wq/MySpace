from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Mission(models.Model):
    mission_taker = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now())
    accept_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='mission_images/', blank=True, null=True)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
