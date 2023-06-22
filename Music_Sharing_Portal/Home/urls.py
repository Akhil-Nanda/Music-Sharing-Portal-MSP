from django.urls import path
from . import views

app_name = 'Home'

urlpatterns = [
    path('', views.index, name='index'),  # url for file uploading
    path('public/', views.public_audio_files, name='public_files'),
    path('private/', views.private_audio_files, name='private'),
    path('protected/', views.protected_audio_files, name='protected'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('delete/<int:file_id>', views.delete_file, name='delete'),
    path('delete/protected/<int:file_id>', views.delete_file, name='protected_delete'),
    path('delete/<int:file_id>/<int:user_id>', views.delete_file, name='public_delete'),
]
