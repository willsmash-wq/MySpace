from django.db import models

# Create your models here.
from django.db import models
from django.forms import forms
# 导入内建的User模型
from django.contrib.auth.models import User
from django.utils import timezone
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from ckeditor.fields import RichTextField

# 任务数据模型
class Mission(models.Model):
    # 任务接收者。参数on_delete 用于指定数据删除的方式，避免两个关联表数据不一致
    mission_taker = models.ForeignKey(User, on_delete=models.CASCADE)

    # 任务标题
    title = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    # 正文
    body = RichTextField()


    created = models.DateTimeField(default=timezone.now())

    # 任务接受时间 参数 auto_now=True 指定每次数据更新时自动写入当前时间
    accept_date = models.DateTimeField(auto_now=True)

    # 内部类class Meta用于给model定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # ’-created‘ 表明数据应该以倒叙排列
        ordering = ('-created',)


    def __str__(self):
        return self.title
