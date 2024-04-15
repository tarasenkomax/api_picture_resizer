# Generated by Django 3.2.9 on 2024-04-15 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image_app', '0006_alter_picture_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='picture',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='parent_picture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childs', to='image_app.picture', verbose_name='Родительское изображение'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(upload_to='', verbose_name='Изображение'),
        ),
    ]