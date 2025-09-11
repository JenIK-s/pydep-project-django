from django.contrib import admin

from .models import FilesProject


@admin.register(FilesProject)
class FilesProjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
