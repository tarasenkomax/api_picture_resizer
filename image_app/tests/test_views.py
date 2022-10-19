from django.test import TestCase
from django.urls import reverse
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
            'url': 'https://autoprodaga.com/auto/auto_red.jpg',
            'width': 300,
            'height': 225,
        }
        Picture.objects.create(**self.test_picture_data)

    def test_view_url_exists_at_desired_location(self):
        responce = self.client.get('/api/images/')
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name(self):
        responce = self.client.get(reverse('image_app:picture_list'))
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_get_validate_data(self):
        responce = self.client.get(reverse('image_app:picture_list'))
        pictures = Picture.objects.all()
        serializer = ListPictureSerializer(pictures, many=True)
        self.assertEqual(responce.data, serializer.data)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_create_picture_from_link(self):
        response = self.client.post(reverse('image_app:picture_list'), format='json', data=self.test_picture_data_2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'auto_red.jpg')
        self.assertEqual(response.data['url'], self.test_picture_data_2['url'])
        self.assertEqual(response.data['width'], self.test_picture_data_2['width'])
        self.assertEqual(response.data['height'], self.test_picture_data_2['height'])

    # def test_create_picture_from_file(self):
    #     pass

    def test_create_picture_with_two_empty_fields(self):
        response = self.client.post(reverse('image_app:picture_list'), format='json', data={})
        #  self.assertEqual(response.data['__empty__'], 'Empty fields')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_picture_with_two_filled_fields(self):
    #     pass


class PictureDetailView(TestCase):
    def setUp(self):
        self.test_picture_data = {
            'name': 'Picture name',
            'url': 'https://autoprodaga.com/auto/auto_red.jpg',
            'width': 500,
            'height': 600,
        }
        picture = Picture.objects.create(**self.test_picture_data)
        self.picture_id = picture.id

    def test_view_url_exists_at_desired_location(self):
        responce = self.client.get(f'/api/images/{self.picture_id}/')
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name(self):
        responce = self.client.get(reverse('image_app:picture_detail', kwargs={'id': self.picture_id}))
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_delete_picture(self):
        response = self.client.delete(reverse('image_app:picture_detail', kwargs={'id': self.picture_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_picture(self):
        response = self.client.delete(reverse('image_app:picture_detail', kwargs={'id': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_detail_invalid_picture_info(self):
        responce = self.client.get(reverse('image_app:picture_detail', kwargs={'id': 999}))
        self.assertEqual(responce.status_code, status.HTTP_404_NOT_FOUND)


class ResizePicture(TestCase):
    def setUp(self):
        self.test_picture_data = {
            'name': 'Picture name',
            'url': 'https://autoprodaga.com/auto/auto_red.jpg',
            'width': 500,
            'height': 600,
        }
        Picture.objects.create(**self.test_picture_data)

    # def test_resize_picture(self):
    #     pass

    def test_resize_invalid_picture(self):
        response = self.client.post(reverse('image_app:picture_resize', kwargs={'id': 999}), format='json',
                                    data={'width': 400, 'height': 300})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

