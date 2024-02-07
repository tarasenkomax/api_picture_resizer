import os

from PIL import Image
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from image_app.exceptions import OpenImageFromException
from image_app.mixins import PictureResizer
from image_app.models import Picture
from image_app.serializers import ListPictureSerializer, CreatePictureSerializer, ResizePictureSerializer


class PictureViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet,
                     PictureResizer):
    queryset = Picture.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListPictureSerializer
        elif self.action == 'create':
            return CreatePictureSerializer
        elif self.action == 'resize':
            return ResizePictureSerializer

    @swagger_auto_schema(
        request_body=CreatePictureSerializer,
        responses={'201': ListPictureSerializer()},
    )
    def create(self, request, *args, **kwargs) -> Response:
        """ Добавление изображений """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.FILES.get('file'):
            request_file = request.FILES.get('file')
            picture = Picture.objects.create_to_file(request_file)
            return Response(data=ListPictureSerializer(picture, many=False).data, status=status.HTTP_201_CREATED, )

        elif serializer.data.get('url'):
            try:
                picture = Picture.objects.create_to_url(serializer.data.get('url'))
            except OpenImageFromException:
                return Response(data={'error': 'Unable to open image'}, status=status.HTTP_400_BAD_REQUEST, )
            return Response(data=ListPictureSerializer(picture, many=False).data, status=status.HTTP_201_CREATED, )

    @swagger_auto_schema(request_body=ResizePictureSerializer, responses={'200': ListPictureSerializer()})
    @action(detail=True, methods=['POST'])
    def resize(self, request, *args, **kwargs):
        serializer = ResizePictureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parent_picture = Image.open(self.get_object().picture)
        width = serializer.data['width'] or int(parent_picture.size[0])
        height = serializer.data['height'] or int(parent_picture.size[1])
        parent_picture_extension = os.path.splitext(str(self.get_object().picture))[1]
        image_name = f'{self.get_object().name}_{serializer.data["width"] or 0}_{serializer.data["height"] or 0}{parent_picture_extension}'

        self.resize_and_save_picture(
            picture=parent_picture,
            width=width,
            height=height,
            image_name=image_name,
        )

        picture = Picture.objects.create(
            name=image_name,
            url=self.get_object().url,
            picture=f"site_media/{image_name}",
            width=width,
            height=height,
            parent_picture=self.get_object(),
        )

        return Response(
            data=ListPictureSerializer(picture, many=False).data,
            status=status.HTTP_201_CREATED,
        )
