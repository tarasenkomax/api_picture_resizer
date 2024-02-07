import os
from urllib.parse import urlparse

import requests
from PIL import Image
from django.db import models
from django.utils.safestring import mark_safe

from image_app.exceptions import OpenImageFromException


class PictureManager(models.Manager):
    @staticmethod
    def create_to_url(url: str) -> 'Picture':
        """ Создание изображения по URL """
        resp = requests.get(url, stream=True).raw
        try:
            img = Image.open(resp)
        except IOError:
            raise OpenImageFromException

        parsed_url = urlparse(url)
        img_name = os.path.basename(parsed_url.path)
        img.save(f'm/site_media/{img_name}')

        picture_obj = Picture.objects.create(
            name=img_name,
            url=url,
            picture=f"site_media/{img_name}",
            width=img.size[0],
            height=img.size[1],
        )
        return picture_obj

    @staticmethod
    def create_to_file(file) -> 'Picture':
        """ Создание изображения по файлу """
        request_picture_size = Image.open(file).size
        picture = Picture.objects.create(
            name=file.name,
            picture=file,
            width=request_picture_size[0],
            height=request_picture_size[1],
        )
        return picture


class Picture(models.Model):
    """ Изображение """
    name = models.CharField(max_length=100, verbose_name='Название')
    url = models.URLField(null=True, blank=True, verbose_name='Ссылка на изображение')
    picture = models.ImageField(upload_to='site_media/', verbose_name='Изображение')
    width = models.PositiveIntegerField(verbose_name='Ширина')
    height = models.PositiveIntegerField(verbose_name='Высота')
    parent_picture = models.ForeignKey('Picture', null=True, blank=True, on_delete=models.CASCADE,
                                       verbose_name='Родительское изображение', related_name='parent')

    def image_tag(self):
        return mark_safe(f'<img src="{self.picture.url}" style= height:100px; object-fit:cover"/>')

    image_tag.short_description = "Изображение"

    def __str__(self):
        return self.name

    objects = PictureManager()

    class Meta:
        verbose_name_plural = 'Изображения'
        verbose_name = 'Изображение'
