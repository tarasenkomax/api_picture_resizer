from django.test import TestCase

from image_app.models import Picture


class PictureModelTest(TestCase):

    def setUp(self):
        self.test_picture_data = {
            'name': 'Picture name',
            'url': 'https://autoprodaga.com/auto/auto_red.jpg',
            'width': 500,
            'height': 600,
        }

    def test_object_name(self):
        picture = Picture.objects.create(**self.test_picture_data)
        self.assertEquals(picture.__str__(), 'Picture name')
