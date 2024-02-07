import os
from urllib.parse import urlparse

import requests
from PIL import Image
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from image_app.models import Picture
from image_app.serializers import ListPictureSerializer, CreatePictureSerializer, ResizePictureSerializer


class PictureViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Picture.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListPictureSerializer
        elif self.action == 'create':
            return CreatePictureSerializer
        elif self.action == 'resize':
            return ResizePictureSerializer

    serializer_class = ListPictureSerializer

    @swagger_auto_schema(request_body=CreatePictureSerializer, responses={'201': ListPictureSerializer()})
    def create(self, request, *args, **kwargs) -> Response:
        """ Создание объекта изображения """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.FILES.get('file'):
            request_file = request.FILES.get('file')
            request_picture_size = Image.open(request_file).size
            picture = Picture.objects.create(name=request_file.name, picture=request_file,
                                             width=request_picture_size[0], height=request_picture_size[1])
            return Response(ListPictureSerializer(picture, many=False).data, status=status.HTTP_201_CREATED)

        elif serializer.data.get('url'):
            resp = requests.get(serializer.data.get('url'), stream=True).raw
            try:
                img = Image.open(resp)
            except IOError:
                return Response({'error': 'Unable to open image'})

            parsed_url = urlparse(serializer.data.get('url'))
            img_name = os.path.basename(parsed_url.path)
            img.save(f'm/site_media/{img_name}')

            picture = Picture.objects.create(name=img_name, url=serializer.data.get('url'),
                                             picture=f"site_media/{img_name}", width=img.size[0], height=img.size[1])
            return Response(ListPictureSerializer(picture, many=False).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ResizePictureView(generics.CreateAPIView):
    """ Изменение размера изображения """
    lookup_field = 'id'
    serializer_class = ResizePictureSerializer

    def get_object(self):
        return get_object_or_404(Picture, id=self.kwargs['id'])

    @staticmethod
    def _resize_and_save_picture(picture: Image, width: int, height: int, image_name: str) -> None:
        """ Изменить размер изображения и сохранить на диск """
        resized_image = picture.resize((width, height))
        resized_image.save(f'm/site_media/{image_name}')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parent_picture = Image.open(self.get_object().picture)
        width = serializer.data['width'] or int(parent_picture.size[0])
        height = serializer.data['height'] or int(parent_picture.size[1])
        parent_picture_extension = os.path.splitext(str(self.get_object().picture))[1]
        image_name = f'{self.get_object().name}_{serializer.data["width"] or 0}_{serializer.data["height"] or 0}{parent_picture_extension}'

        self._resize_and_save_picture(picture=parent_picture, width=width, height=height, image_name=image_name)

        picture = Picture.objects.create(name=image_name, url=self.get_object().url, picture=f"site_media/{image_name}",
                                         width=width, height=height, parent_picture=self.get_object())
        return Response(ListPictureSerializer(picture, many=False).data)
