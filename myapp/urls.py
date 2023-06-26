from django.urls import path
from . import views
# 正在部署的应用的名称
app_name = 'myapp'
urlpatterns = [
    # path函数将url映射到视图
    path('list/', views.mission_list, name='mission_list'),
    path('mission_detail/<int:id>/', views.mission_detail, name='mission_detail'),
    path('mission_create/', views.mission_create, name="mission_create"),
    path('mission_delete/<int:id>', views.mission_delete, name="mission_delete"),
    path('mission_update/<int:id>/', views.mission_update, name="mission_update"),
    path('comment_delete/<int:id>/', views.comment_delete, name="comment_delete"),
    path('mission_rating/<int:id>/', views.mission_rating, name='mission_rating'),
]