from django.db import models


class Picture(models.Model):
    """ Изображение """
    name = models.CharField(max_length=100, verbose_name='Название')
    url = models.URLField(null=True, blank=True)
    picture = models.ImageField(upload_to='site_media/')
    width = models.IntegerField(verbose_name='Ширина')
    height = models.IntegerField(verbose_name='Высота')
    parent_picture = models.IntegerField(null=True, blank=True, verbose_name='ID Родительского изображения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Изображения'
        verbose_name = 'Изображение'
