from . models import Networks
from rest_framework import serializers


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
