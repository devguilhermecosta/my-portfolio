from rest_framework import serializers
from collections import defaultdict
from . models import Work, WorkImage


class WorkImageSerializer(serializers.ModelSerializer):
    url = serializers.StringRelatedField(source='image')

    class Meta:
        model = WorkImage
        fields = [
            'id',
            'url',
        ]

    def validate(self, attrs) -> None:
        _errors = defaultdict(list)

        for field, value in attrs.items():
            if not value or value == '':
                _errors[field].append(
                    'Campo obrigatório',
                )

        if _errors:
            raise serializers.ValidationError(_errors)

        return super().validate(attrs)


class WorkSerializer(serializers.ModelSerializer):
    images = WorkImageSerializer(
        many=True,
        source='workimages',
    )

    class Meta:
        model = Work
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'link',
            'cover',
            'created_at',
            'images',
        ]
