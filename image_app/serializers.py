from rest_framework import serializers

from image_app.models import Picture


class ListPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'name', 'url', 'picture', 'width', 'height', 'parent_picture']


class CreatePictureSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(required=False)
    url = serializers.URLField(required=False)

    class Meta:
        model = Picture
        fields = ['file', 'url']

    def validate(self, data):
        url = data.get('url')
        file = data.get('file')
        if url and file:
            raise serializers.ValidationError(detail={'__all__': 'Two fields'})
        if not url and not file:
            raise serializers.ValidationError(detail={'__empty__': 'Empty fields'})
        return data


class ResizePictureSerializer(serializers.ModelSerializer):
    height = serializers.IntegerField(default=0)
    width = serializers.IntegerField(default=0)

    class Meta:
        model = Picture
        fields = ['height', 'width']

    def validate(self, data):
        height = data.get('height')
        width = data.get('width')
        if not height and not width:
            raise serializers.ValidationError(detail={'__empty__': 'Empty fields'})
        return data
