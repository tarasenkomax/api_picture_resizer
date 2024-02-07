from PIL import Image


class PictureResizer:
    @staticmethod
    def resize_and_save_picture(
            picture: Image,
            width: int,
            height: int,
            image_name: str,
    ) -> None:
        """
        Изменить размер изображения и сохранить на диск
        :param picture: (Image) Изображение
        :param width: (int) Ширина
        :param height: (int) Высота
        :param image_name: (str) Имя изображения
        :return: None
        """
        resized_image = picture.resize((width, height))
        resized_image.save(f'm/site_media/{image_name}')
