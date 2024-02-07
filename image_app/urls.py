from django.urls import path
from rest_framework.routers import DefaultRouter

from image_app.views import ResizePictureView, PictureViewSet

app_name = "image_app"

router = DefaultRouter()

router.register('', PictureViewSet, basename='picture')

urlpatterns = [
    path('<int:id>/resize', ResizePictureView.as_view(), name='picture_resize'),
]
urlpatterns += router.urls
