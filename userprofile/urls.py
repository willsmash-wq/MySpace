from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns=[
   path('api/registered_users/', views.registered_users, name='registered_users'),
   path('login/', views.user_login, name='login'),
   path('register/', views.user_register, name="register"),
   path('logout/', views.user_logout, name="logout"),
   path('delete/<int:id>/', views.user_delete, name='delete'),
   path('edit/<int:id>/', views.profile_edit, name='edit'),
]