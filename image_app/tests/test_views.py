from django.test import TestCase
from rest_framework import status

from image_app.models import Picture
from image_app.serializers import ListPictureSerializer


class PictureViewTest(TestCase):
    def setUp(self):
        self.test_picture_data = {
            'url': 'https://images.drive.ru/i/0/4efb6bde09b6028018000876.jpg',
            'width': 320,
            'height': 240,
        }
        self.test_picture_data_2 = {
            'url': 'https://cs14.pikabu.ru/avatars/503/x503842-1468369487.png',
            'width': 256,
            'height': 256,
        }
        picture = Picture.objects.create(**self.test_picture_data)
        Picture.objects.create(**self.test_picture_data_2)
        self.picture_id = picture.id

    def test_pictures_list_view(self):
        response = self.client.get('/api/images/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_validate_data(self):
        response = self.client.get('/api/images/')
        pictures = Picture.objects.all()
        serializer = ListPictureSerializer(pictures, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_picture_from_url(self):
        response = self.client.post(
            path='/api/images/',
            format='json',
            data=self.test_picture_data_2,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'x503842-1468369487.png')
        self.assertEqual(response.data['url'], self.test_picture_data_2['url'])
        self.assertEqual(response.data['width'], self.test_picture_data_2['width'])
        self.assertEqual(response.data['height'], self.test_picture_data_2['height'])

    def test_create_picture_from_file(self):
        pass

    def test_create_picture_with_two_empty_fields(self):
        response = self.client.post(
            path='/api/images/',
            format='json',
            data={})
        #  self.assertEqual(response.data['__empty__'], 'Empty fields')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_picture_with_two_filled_fields(self):
        pass

    def test_delete_picture_view(self):
        response = self.client.delete(f'/api/images/{self.picture_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_picture(self):
        response = self.client.delete(f'/api/images/{999}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resize_picture(self):
        pass

    def test_resize_invalid_picture(self):
        response = self.client.post(
            path='/api/images/999/resize/',
            format='json',
            data={
                'width': 400,
                'height': 300,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
