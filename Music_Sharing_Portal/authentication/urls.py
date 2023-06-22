from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('success/', views.success, name='success'),
    path('verification-error/', views.error, name='error'),
]
