from rest_framework import serializers
from . models import Work, WorkImage


class WorkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkImage
        fields = [
            'id',
            'work',
            'image',
        ]


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'link',
            'cover',
            'images',
            'created_at',
        ]

    images = serializers.HyperlinkedRelatedField(
        queryset=WorkImage.objects.all(),
        view_name='work-images',
        many=True,
    )
