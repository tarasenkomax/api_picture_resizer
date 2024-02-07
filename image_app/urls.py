from rest_framework.routers import DefaultRouter

from image_app.views import PictureViewSet

app_name = "image_app"

router = DefaultRouter()

router.register('', PictureViewSet, basename='picture')

