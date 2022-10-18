from django.db import models


class Picture(models.Model):
    """ Изображение """
    name = models.CharField(max_length=100, verbose_name='Название')
    url = models.URLField(null=True, blank=True, verbose_name='Ссылка на изображение')
    picture = models.ImageField(upload_to='site_media/', blank=True, null=True, verbose_name='Изображение')
    width = models.PositiveIntegerField(verbose_name='Ширина')
    height = models.PositiveIntegerField(verbose_name='Высота')
    parent_picture = models.ForeignKey('Picture', null=True, blank=True, on_delete=models.CASCADE,
                                       verbose_name='Родительское изображение', related_name='parent')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Изображения'
        verbose_name = 'Изображение'
