import os
from urllib.parse import urlparse
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from PIL import Image
import requests

from image_app.models import Picture
from image_app.serializers import ListPictureSerializer, CreatePictureSerializer, ResizePictureSerializer


class PictureView(generics.ListAPIView, generics.CreateAPIView):
    """
    (GET) Получение списка доступных изображений
    (POST) Добавление изображений
    """
    queryset = Picture.objects.all()
    serializer_class = CreatePictureSerializer

    def get(self, request, *args, **kwargs):
        return Response(ListPictureSerializer(self.get_queryset(), many=True).data)

    def create(self, request, *args, **kwargs):
        """Создание объекта изображения"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.FILES.get('file'):
            request_picture = Image.open(request.FILES.get('file'))
            picture = Picture.objects.create(name=request.FILES.get('file').name,
                                             picture=request.FILES.get('file'),
                                             width=request_picture.size[0],
                                             height=request_picture.size[1])
            return Response(ListPictureSerializer(picture, many=False).data)
        elif serializer.data.get('url'):
            resp = requests.get(serializer.data.get('url'), stream=True).raw
            try:
                img = Image.open(resp)
            except IOError:
                return Response({'error': 'Unable to open image'})

            parsed_url = urlparse(serializer.data.get('url'))
            img_name = os.path.basename(parsed_url.path)
            img.save(f'site_media/{img_name}')

            picture = Picture.objects.create(
                name=img_name,
                url=serializer.data.get('url'),
                picture=f"site_media/{img_name}",
                width=img.size[0],
                height=img.size[1], )
            return Response(ListPictureSerializer(picture, many=False).data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PictureDetailView(generics.RetrieveDestroyAPIView):
    """
    (GET) Получение детальной информации о изображении
    (DEL) Удаление
    """
    queryset = Picture.objects.all()
    serializer_class = ListPictureSerializer
    lookup_field = 'id'


class ResizePicture(generics.CreateAPIView):
    """
    (POST) Изменение размера изображения
    """
    lookup_field = 'id'
    serializer_class = ResizePictureSerializer

    def get_object(self):
        return get_object_or_404(Picture, id=self.kwargs['id'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent_picture = Image.open(self.get_object().picture)
        width = serializer.data['width'] or int(parent_picture.size[0])
        height = serializer.data['height'] or int(parent_picture.size[1])
        resized_image = parent_picture.resize((width, height))
        file_extension = os.path.splitext(str(self.get_object().picture))[1]  # формат родительского изображения
        name_image = f'{self.get_object().name}_{serializer.data["width"] or 0}_{serializer.data["height"] or 0}{file_extension}'
        resized_image.save(f'site_media/{name_image}')

        picture = Picture.objects.create(
            name=name_image,
            url=self.get_object().url,
            picture=f"site_media/{name_image}",
            width=width,
            height=height,
            parent_picture=self.kwargs['id'])
        return Response(ListPictureSerializer(picture, many=False).data)
