from django.contrib import admin

# Register your models here.
from django.contrib import admin
#导入ArticlePost
from .models import Mission
from django_summernote.admin import SummernoteModelAdmin

class MissionAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Mission, MissionAdmin)
# 将ArticlePost注册到admin中
