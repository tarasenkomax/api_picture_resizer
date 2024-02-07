from django.contrib import admin
from .models import Picture


class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'image_tag', 'width', 'height', 'parent_picture')
    list_display_links = ('name',)


admin.site.register(Picture, PictureAdmin)
