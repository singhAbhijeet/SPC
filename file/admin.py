from django.contrib import admin
from .models import File , FileField , Folder
# Register your models here.
admin.site.register(File)
admin.site.register(FileField)
admin.site.register(Folder)