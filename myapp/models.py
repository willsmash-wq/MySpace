from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class Mission(models.Model):
    mission_taker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taken_missions')
    title = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    body = CKEditor5Field('body', config_name='extends')
    created = models.DateTimeField(default=timezone.now())
    accept_date = models.DateTimeField(auto_now=True)
    rating_users = models.ManyToManyField(User, through='MissionRating', related_name='rated_missions')

    ARTICLE_TYPE_CHOICES = (
        ('销售支撑网类', '销售支撑网类'),
        ('认领规则类', '认领规则类'),
        ('每周实例新建类', '每周实例新建类'),
        ('月度稽核类', '月度稽核类'),
        ('代码类', '代码类'),
        ('虚拟类', '虚拟类'),
        ('问答类', '问答类'),
    )
    article_type = models.CharField(max_length=20, choices=ARTICLE_TYPE_CHOICES, default='虚拟类')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title



class Comment(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)


class MissionRating(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    class Meta:
        unique_together = ('mission', 'user')  # 保证每个用户对同一个任务只能评分一次
