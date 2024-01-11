from rest_framework import serializers
from . models import Work, WorkImage


class WorkImageSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(
        source='image',
        required=True,
        error_messages={
            'required': 'Campo obrigatório',
            'invalid': 'Envie somente imagens',
        })

    work_id = serializers.PrimaryKeyRelatedField(
            source='work',
            queryset=Work.objects.all(),
            error_messages={
                'required': 'Campo obrigatório',
                'blank': 'Campo obrigatório',
                'null': 'Campo obrigatório',
            }
        )

    class Meta:
        model = WorkImage
        fields = [
            'id',
            'work_id',
            'url',
        ]


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
            'is_published',
            'show_in_home'
        ]

    def validate_title(self, value: str) -> str:
        work = Work.objects.filter(title=value.lower())

        if work:
            raise serializers.ValidationError(
                'work com este title já existe',
                code='unique',
            )

        return value.lower()
