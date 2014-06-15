from django.contrib import admin
from imagekit.admin import AdminThumbnail
from models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('description', 'created_time', 'publish_time', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='header_image_thumbnail')

admin.site.register(News, NewsAdmin)
