from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

# Create your models here.


class News(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    publish_time = models.DateTimeField(auto_now_add=True)

    description = models.TextField(default="")
    content = models.TextField(blank=True, default="")

    header_image = models.ImageField(upload_to='photos')
    header_image_thumbnail = ImageSpecField([ResizeToFill(50, 50)], image_field='header_image', format='png')
    header_image_display = ImageSpecField([ResizeToFill(170, 115)], image_field='header_image', format='png')


