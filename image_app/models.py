import os
from typing import Optional
from urllib.parse import urlparse

import requests
from django.db import models
from django.utils.safestring import mark_safe
from PIL import Image

from image_app.exceptions import OpenImageFromUrlException
from image_app.utils import resize_and_save_picture


class PictureManager(models.Manager):
    @staticmethod
    def create_to_url(url: str) -> 'Picture':
        """ Создание изображения по URL """
        resp = requests.get(url, stream=True).raw
        try:
            img = Image.open(resp)
        except IOError:
            raise OpenImageFromUrlException

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
    parent_picture = models.ForeignKey(
        to='Picture',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Родительское изображение',
        related_name='parent',
    )

    def __str__(self):
        return self.name

    def create_resized_image(
            self,
            width: Optional[int] = None,
            height: Optional[int] = None,
    ) -> 'Picture':
        """ Изменение размера текущего изображения и сохранение как отдельный объект 'Picture' """
        parent_picture = self.picture
        new_width = width or int(parent_picture.size[0])
        new_height = height or int(parent_picture.size[1])
        parent_picture_extension = os.path.splitext(str(parent_picture))[1]
        image_name = f'{self.name}_{width or 0}_{height or 0}{parent_picture_extension}'

        resize_and_save_picture(
            picture=Image.open(parent_picture),
            width=width,
            height=height,
            image_name=image_name,
        )

        picture_obj = Picture.objects.create(
            name=image_name,
            url=self.url,
            picture=f"site_media/{image_name}",
            width=new_width,
            height=new_height,
            parent_picture=self,
        )
        return picture_obj

    def image_tag(self):
        return mark_safe(f'<img src="{self.picture.url}" style= height:100px; object-fit:cover"/>')

    image_tag.short_description = "Изображение"

    objects = PictureManager()

    class Meta:
        verbose_name_plural = 'Изображения'
        verbose_name = 'Изображение'
