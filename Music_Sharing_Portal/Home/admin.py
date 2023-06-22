from django.contrib import admin
from . models import AudioFiles,ProtectedFiles
# Register your models here.
admin.site.register(AudioFiles)
admin.site.register(ProtectedFiles)