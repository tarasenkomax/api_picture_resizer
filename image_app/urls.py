from django.urls import path

from image_app.views import PictureView, PictureDetailView, ResizePicture

app_name = "image_app"

urlpatterns = [
    path('', PictureView.as_view(), name='picture_list'),
    path('<int:id>/', PictureDetailView.as_view(), name='picture_detail'),
    path('<int:id>/resize', ResizePicture.as_view(), name='picture_resize'),

]

