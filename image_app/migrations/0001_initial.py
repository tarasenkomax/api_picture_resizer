# Generated by Django 3.2.9 on 2021-11-02 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('url', models.URLField(null=True)),
                ('picture', models.ImageField(upload_to='')),
                ('width', models.IntegerField(verbose_name='Ширина')),
                ('height', models.IntegerField(verbose_name='Высота')),
                ('parent_picture', models.IntegerField(null=True, verbose_name='ID Родительского изображения')),
            ],
        ),
    ]
