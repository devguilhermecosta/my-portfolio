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
    title = serializers.CharField(
        max_length=255,
        error_messages={
            'required': 'Campo obrigatório',
            'blank': 'Campo obrigatório',
            'invalid': 'Envie somente textos',
        }
    )

    description = serializers.CharField(
        max_length=1250,
        error_messages={
            'required': 'Campo obrigatório',
            'blank': 'Campo obrigatório',
            'invalid': 'Envie somente textos',
        }
    )

    cover = serializers.ImageField(
        error_messages={
            'required': 'Campo obrigatório',
            'invalid': 'Envie somente imagens',
        }
    )

    images = WorkImageSerializer(
        many=True,
        source='workimages',
        required=False,
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

    def validate_title(self, value: str) -> str:
        work = Work.objects.filter(title=value.lower())

        if work:
            raise serializers.ValidationError(
                'work com este title já existe',
                code='unique',
            )

        return value.lower()
