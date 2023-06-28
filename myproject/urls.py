"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from django.conf import settings
from django.views.static import serve
from django.views.static import serve
from . import views
from .views import IndexView
from django.conf.urls.static import static

urlpatterns = [
                  path('myapp/', include('myapp.urls')),
                  path('admin/', admin.site.urls),
                  path('userprofile/', include('userprofile.urls', namespace='userprofile')),
                  path('', views.shou, name='shou'),
                  path('captcha/', include('captcha.urls')),  # 图片验证码 路由
                  path('refresh_captcha/', views.refresh_captcha, name='refresh_captcha'),  # 刷新验证码，ajax
                  path('test/', IndexView.as_view(), name='test'),  # get与post请求路径
                  path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
