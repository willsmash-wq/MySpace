import datetime

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    department = models.CharField(max_length=100, default='虚拟部门')
    team = models.CharField(max_length=100, blank=True, null=True)
    team_leader = models.BooleanField(default=False)

    def __str__(self):
        return 'user{}'.format(self.user.username)

    def clean(self):
        if self.team_leader and not self.team:
            raise ValidationError("只有选择了团队的用户才能成为团队领导者")
        if self.team_leader:
            existing_team_leader = Profile.objects.filter(team=self.team, team_leader=True).exclude(id=self.id).first()
            if existing_team_leader:
                raise ValidationError(f"团队 {self.team} 已经有一个领导者： {existing_team_leader.user.username}")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Keywork(models.Model):
    year = models.IntegerField(default=datetime.datetime.now().year)
    month = models.IntegerField(default=datetime.datetime.now().month)
    team = models.CharField(max_length=100)
    content = models.TextField()
    last_edit_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.year}-{self.month} {self.team}'
