from . models import Networks
from rest_framework import serializers
from collections import defaultdict


class NetworksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Networks
        fields = [
            'instagram',
            'linkedin',
            'github',
            'whatsapp',
            'phone',
            'email',
        ]

    def validate(self, attrs):
        _errors = defaultdict(list)

        for field, value in attrs.items():
            if not value or value == '':
                _errors[field].append(
                    'Campo obrigatório',
                )

        if _errors:
            raise serializers.ValidationError(_errors)

        return super().validate(attrs)
